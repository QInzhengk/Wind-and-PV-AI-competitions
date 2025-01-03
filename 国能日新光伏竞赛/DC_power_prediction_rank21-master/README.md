# DataCastle国能日新光伏功率预测

## 数据异常处

本题在测试集中提供了**时间、辐照度、风速、风向、温度、压强、湿度、实发辐照度** 8个特征，以及标签**实际功率**。
而在训练集中只有前七个特征，无**实发辐照度**。

## 策略

在观察了数据之后，我们确定实发辐照度是一个强力特征，于是我们采取了分部训练的策略：

1. 第一次训练以**实发辐照度**为**标签**，预测 **测试集的实发辐照度**

2. 第二次训练将**实发辐照度**加入**特征**进行训练，预测最终的标签**实际功率**

## 特征工程

由于数据具有周期性，于是我们提取每天的数据，并以**辐照度**为依据，构建**白天(daytime)**和**夜晚(nighttime)**以及**整日(allday)**三种时间分区，并对各个时间分区构建**mean/std/min/max**以及**var(max-min)**,通过对构造特征进行**加减乘除**来构造新的特征。

## 模型选择

选择了lightGbm以及xgboost进行融合,由于最后时间不够，所以我们仅尝试了简单的加权融合。最后阶段尝试使用Lstm发现效果不好，故放弃使用。

## 分析

1. 由于辐照度是人工预测，会带来误差，所以预测的实发辐照度也存着误差。
2. 有的电场的实际功率在夜晚直接为0，有的电场会由于消耗得到负值，所以我们进行了特殊化处理(specialize)
3. 在数据预处理阶段需要做的更加仔细，原始数据的时间在.csv打开之后呈现整数，实际上在控制台打印发现为小数(例如可能看到的0 ：00实际为23 : 59.99)，这样导致提取出来的时间会有很大错误，为后面的运算带来非常大的误差。

## 总结

这次最深的感受还是那句老话**特征为王**，只有特征才能带来极大的提分上限，同时，数据预处理的重要性大于模型融合。

[博客链接](https://blog.csdn.net/yyhhlancelot/article/details/84568016)
