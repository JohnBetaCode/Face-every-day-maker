#  ----------------------------------------------------------------------
# Clear std out
clear

echo  "Checking black python format"
# python3 -m black /workspace/dev_ws/src/ --check --exclude="background_removal" || true
python3 -m black /workspace/dev_ws/src/ --exclude="background_removal" || true
echo  " "

#  ----------------------------------------------------------------------
# Source local enviroment variables
source "${PWD%}/dev_ws/configs/env_vars.sh"

# -----------------------------------------------------------------------
# Run every-day studio
python3 "${PWD%}/dev_ws/src/everyday_studio/every_day_maker.py"

# -----------------------------------------------------------------------
exit 0