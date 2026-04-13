#!/usr/bin/env bash
# Run the Dash/pytest suite in the project environment. Suitable for CI.
# Exit 0 if all tests pass, 1 otherwise.
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT" || exit 1

activate_python_env() {
  if [[ -n "${VENV_PATH:-}" && -f "${VENV_PATH}/bin/activate" ]]; then
    # shellcheck source=/dev/null
    source "${VENV_PATH}/bin/activate"
    return 0
  fi
  if [[ -f "${ROOT}/.venv/bin/activate" ]]; then
    # shellcheck source=/dev/null
    source "${ROOT}/.venv/bin/activate"
    return 0
  fi
  if command -v conda >/dev/null 2>&1; then
    eval "$(conda shell.bash hook)"
    conda activate "${CONDA_ENV_NAME:-quantium-dash}"
    return 0
  fi
  echo "run_tests.sh: no env found. Use .venv, set VENV_PATH, or install conda (default env: quantium-dash)." >&2
  return 1
}

activate_python_env || exit 1

if pytest tests/ -v --headless; then
  exit 0
fi
exit 1
