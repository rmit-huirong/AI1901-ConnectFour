#!/bin/bash          

testAgent () {
    WINS=0
    LOSS=0

    for ((i=1;i<=$2;i++)); do
        OUTPUT=$(pipenv run python -m connectfour.game --player-one $1 --player-two StudentAgent --no-graphics --fast --auto-close | python3 -c "import sys, json; print(json.load(sys.stdin)['winner_id'])")
        if [ $OUTPUT == 2 ]
        then
            ((WINS++))
        else
            ((LOSS++))
        fi
    done

    WINRATE=$((WINS/RANGE*100))
    echo "Winrates against { $1 }-> [ $WINRATE % ]"
}

RANGE=${1:-10}
echo "Run the test with RANGE: [$RANGE]"
testAgent "MonteCarloAgent" $RANGE
testAgent "RandomAgent" $RANGE