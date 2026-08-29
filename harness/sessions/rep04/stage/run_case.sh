#!/bin/bash
# run_case.sh <sid> <pressure_Pa> <ninit> <nprod> <tag> <seed> [grid]
# One RASPA GCMC case.  Writes runs/<tag>/<sid>_<Ptag>_s<seed>[_g]/ and appends one
# CSV line to results/<tag>.csv.  Exits non-zero on failure.
set -u
WS=/home1/users/Bei/ws/rep04
SID=$1; PPA=$2; NINIT=$3; NPROD=$4; TAG=$5; SEED=${6:-0}; GRID=${7:-no}

PTAG=$(python3 -c "print('%g'%($PPA/1e5))")
SUF=""; [ "$GRID" = "yes" ] && SUF="_g"
CASE=$WS/runs/$TAG/${SID}_${PTAG}bar_s${SEED}${SUF}
mkdir -p "$CASE" || exit 1
cd "$CASE" || exit 1

# Resolve sid -> db filename via the manifest map (tab separated).
CIF=$(awk -F'\t' -v s="$SID" '$1==s{print $2}' $WS/manifest/sid_map.tsv)
if [ -z "$CIF" ]; then echo "NOCIF $SID"; exit 2; fi

UC=$(python3 $WS/bin/prep_cif.py "$WS/db/$CIF" "$SID.cif") || exit 3
set -- $UC
UA=$1; UB=$2; UC2=$3

export RASPA_DIR=$WS/raspa_home
GRIDBLOCK=""
if [ "$GRID" = "yes" ]; then
  GF=$WS/grids/UFF/$SID/0.200000/${SID}_CH4_sp3_truncated.grid
  # Grid generation is serialised per structure by an mkdir lock: several cases
  # may want the same grid at once, and a half-written grid is worse than none.
  if [ ! -s "$GF" ]; then
    LOCK=$WS/grids/.lock_$SID
    if mkdir "$LOCK" 2>/dev/null; then
      mkdir -p "$CASE/mkgrid" && cd "$CASE/mkgrid"
      cp ../$SID.cif .
      cat > simulation.input <<EOF
SimulationType                MakeGrid
Forcefield                    UFF
ChargeMethod                  None
CutOff                        12.8
UseChargesFromCIFFile         no
NumberOfGrids                 1
GridTypes                     CH4_sp3
SpacingVDWGrid                0.2

Framework 0
FrameworkName                 $SID
UnitCells                     $UA $UB $UC2
ExternalTemperature           298.0
EOF
      $WS/toolchain/raspa/bin/simulate simulation.input > mkgrid.stdout 2>&1
      cd "$CASE"; rmdir "$LOCK" 2>/dev/null
    else
      # someone else is building it; wait up to 30 min
      for i in $(seq 1 180); do [ -s "$GF" ] && break; sleep 10; done
    fi
  fi
  [ -s "$GF" ] || { echo "NOGRID $SID"; exit 4; }
  GRIDBLOCK="NumberOfGrids 1
GridTypes CH4_sp3
SpacingVDWGrid 0.2
UseTabularGrid yes"
fi

cat > simulation.input <<EOF
SimulationType                MonteCarlo
NumberOfCycles                $NPROD
NumberOfInitializationCycles  $NINIT
PrintEvery                    100000
RestartFile                   no
RandomSeed                    $((SEED+1))

Forcefield                    UFF
ChargeMethod                  None
CutOff                        12.8
UseChargesFromCIFFile         no
$GRIDBLOCK

Framework 0
FrameworkName                 $SID
UnitCells                     $UA $UB $UC2
ExternalTemperature           298.0
ExternalPressure              $PPA

Component 0 MoleculeName             methane
            MoleculeDefinition       TraPPE
            TranslationProbability   1.0
            ReinsertionProbability   1.0
            SwapProbability          2.0
            CreateNumberOfMolecules  0
EOF

T0=$(date +%s)
$WS/toolchain/raspa/bin/simulate simulation.input > raspa.stdout 2>&1
RC=$?
T1=$(date +%s)
rm -rf Movies VTK Restart
python3 $WS/bin/parse_out.py "$CASE" "$SID" "$PPA" "$NINIT" "$NPROD" "$SEED" \
        "$GRID" "$((T1-T0))" "$RC" >> $WS/results/$TAG.csv
gzip -f Output/System_0/*.data 2>/dev/null
exit $RC
