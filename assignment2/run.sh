# SIG=1.0
# # K=1000

# python ./main.py \
#   --algorithm "atg" \
#   --data-dir "data/corel.txt" \
#   --project-name "atg-parameter-sigma${SIG}" \
#   --epsilon  0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 \
#   --alpha   0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 \
#   --delta 0.2  \
#   --sigma ${SIG} 


SIG=1
# cardi="1 2 3 4 5 6 7 8 9 10"
cardi="5"
# K=1000
# alpha="0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75"
eps="0.08 0.10 0.12 0.14 0.16 0.18 0.2"
# eps="0.1"
data_file="data/euallweighted.txt"

# --car-cons ${K} \
# python ./main.py \
#   --algorithm  "atg" \
#   --data-dir "data/corel_1000.txt" \
#   --project-name "expg-debug-corel-200" \
#   --car-cons 100 \
#   --lazy-eval True


python ./experiment.py \
  --algorithm "atg eps-approx expg expgk" \
  --project-name "atg-parameter-sigma${SIG}" \
  --epsilon  ${eps} \
  --exp_par  "epsilon" \
  --alpha   0.1 \
  --delta 0.2  \
  --sigma ${SIG} \
  --car-cons ${cardi} \
  --application 'influmax' \
  --data-dir ${data_file} 