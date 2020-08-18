# Turing test

两部分：30位同学

第一部分：机器写的或者是人写的
1.挑选我们的模型生成的单张图的质量好一点的50篇摘要
2.随意选取数据集给的gt的50篇摘要（不需要对应）
3.打乱顺序让评判者评判每一个样本是否是人写的
4.最后分析gt中有多少被判为人写的，模型生成中有多少被判为人写的

第二部分：哪一个写的更好
1.挑选我们的模型生成的组合图的质量好一点的50篇摘要
2.挑选对应的50篇摘要用SOTA模型生成的（需要对应）
3.让评判者对应两个选择哪一个写的更好（根据语法 流畅度 逻辑）

### Usage

1. test the whole validation

   ```
   python eval.py dataset/single_our.txt dataset/single_gt.txt
   ```

2. choose the top-50 `bleu_4` using the gt; the output file will be saved in the `results`

   ```
   python eval_single.py dataset/single_our.txt dataset/single_gt.txt
   ```

3. choose the top-100 from group_graph

   ```
   python eval_group.py dataset/group_our_1w.txt
   ```

   

