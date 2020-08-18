import os

# with open('./results/single_top_50.txt') as f:
#     top_50 = f.readlines()

# with open('./results/single_random_gt_50.txt') as f:
#     random_50 = f.readlines()  

# for text in top_50:
#     text = text.strip('\n')
#     text = text + '(A) [1分]\n'
#     with open('./results/single_questions.txt', 'a+', encoding='utf-8') as f:
#         f.writelines(text)
#         f.writelines('A. Machine\n')
#         f.writelines('B. Human\n')
#         f.writelines('\n')

# for text in random_50:
#     text = text.strip('\n')
#     text = text + '(B) [1分]\n'
#     with open('./results/single_questions.txt', 'a+', encoding='utf-8') as f:
#         f.writelines(text)
#         f.writelines('A. Machine\n')
#         f.writelines('B. Human\n')
#         f.writelines('\n')

flag = 'group_baseline_50'  # group_top_50, group_baseline_50
with open('./results/{}.txt'.format(flag)) as f:
    group_50 = f.readlines()

for text in group_50:
    text = text.strip('\n')
    if len(text) == 0: continue
    text = text + '[矩阵量表题]\n'
    with open('./results/{}_wenjuanxing.txt'.format(flag), 'a+', encoding='utf-8') as f:
        f.writelines(text)
        f.writelines('1 2 3 4 5\n')
        f.writelines('Grammar\n')
        f.writelines('Coherence\n')
        f.writelines('Informativeness\n')
        f.writelines('\n')