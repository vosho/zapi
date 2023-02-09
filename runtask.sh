path=$(dirname "$0")
cd $path;
if [[ -f "venv/bin/activate" ]]; then
    source venv/bin/activate;
else
    #sconda activate server;
    echo '-'
fi
param=""
if [ "$2" == 'reload' ] || [ "$3" == 'reload' ]; then
    ps=`ps aux|grep "python main.py -c task -n $1" | grep -v "grep"|awk '{print $2}'`
    if [ "$ps" != '' ]; then
        echo "Reloading...";
        kill -9 $ps;
    fi
else
    param="$2"
fi
python main.py -c task -n $1 $param
#'/Users/abw/opt/anaconda3'