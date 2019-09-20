[ $# -lt 1 ] && { echo '第1引数にRSSのURLを指定してください。' 1>&2; exit 1; }
SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd "$SCRIPT_DIR"
python3 get_news.py "$1" "$SCRIPT_DIR"

