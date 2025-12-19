import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import STL
import pmdarima as pm # 需要安装: pip install pmdarima

# 设置全局绘图样式
plt.style.use('seaborn-v0_8')

# ==========================================
# 1. Box and Jenkins Approach (模拟 ARMA)
# ==========================================
print("--- Box and Jenkins Approach ---")
np.random.seed(123)
n = 200

# R: ar=c(0.5, 0.2), ma=c(0.1, 0.6)
# Python Statsmodels 注意: AR 系数在左边时符号要取反
# R: X_t = 0.5*X_{t-1} ... -> Python: X_t - 0.5*X_{t-1} ... = 0
ar_params = np.array([1, -0.5, -0.2])
ma_params = np.array([1, 0.1, 0.6])

# 生成数据
process = ArmaProcess(ar_params, ma_params)
x = process.generate_sample(nsample=n)

# 拟合模型: ARIMA(2,0,2), include.mean=F -> trend='n'
model = ARIMA(x, order=(2, 0, 2), trend='n')
fit = model.fit()

# 获取系数 (Python中系数顺序可能与R不同，通常是 ar1, ar2, ma1, ma2)
# R code logic assumes: p[1]=ar1, p[2]=ar2, p[3]=ma1, p[4]=ma2
params = fit.params
print("Coefficients:", params)

# 手动计算残差 (Replicating the loop logic)
# 注意：Python索引从0开始
Z = np.zeros(n)
# 对应 R 的 loop 3:n (Python index 2 到 n-1)
# 我们使用拟合出的系数进行计算
p = params # ar_L1, ar_L2, ma_L1, ma_L2
for j in range(2, n):
    # Python ARIMA params: prediction = ar1*x_{t-1} + ar2*x_{t-2} + ma1*Z_{t-1} + ma2*Z_{t-2}
    # Z[j] = Observed - Predicted
    pred_val = p[0]*x[j-1] + p[1]*x[j-2] + p[2]*Z[j-1] + p[3]*Z[j-2]
    Z[j] = x[j] - pred_val

# 手动预测 (Manual Forecast)
# R: n (最后一天). Python index: n-1
last_x = x[n-1]
prev_x = x[n-2]
last_Z = Z[n-1]
prev_Z = Z[n-2]

# 往前预测 1 步 (Pred1)
Pred1 = p[0]*last_x + p[1]*prev_x + p[2]*last_Z + p[3]*prev_Z

# 往前预测 2 步 (Pred2)
# 下一步的 Z 设为 0 (期望值)
Pred2 = p[0]*Pred1 + p[1]*last_x + p[2]*0 + p[3]*last_Z

print(f"Manual Pred1: {Pred1}")
print(f"Manual Pred2: {Pred2}")

# 使用内置函数预测
builtin_pred = fit.forecast(steps=2)
print("Built-in Predict:\n", builtin_pred)
print("\n")


# ==========================================
# 2. Treasury Bill Example
# ==========================================
print("--- Treasury Bill Example ---")

# --- 数据加载 (如果没有文件，使用模拟数据) ---
try:
    # 假设数据格式是简单的数值文本
    # ttbill = pd.read_csv("ustbill.dat", sep="\s+", header=None).iloc[:, 1:].values.flatten()
    # 为了演示，生成一段类似的随机漫步数据
    dummy_dates = pd.date_range(start='1990-01-01', periods=500, freq='D')
    ttbill = np.exp(np.cumsum(np.random.normal(0, 0.01, 500))) # 模拟数据
except:
    ttbill = np.array([]) 

# 绘图
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].plot(ttbill)
axes[0, 0].set_title("Raw Data")
plot_acf(ttbill, ax=axes[0, 1], title="ACF Raw")

lntbill = np.log(ttbill)
axes[1, 0].plot(lntbill)
axes[1, 0].set_title("Log Data")
plot_acf(lntbill, ax=axes[1, 1], title="ACF Log")
plt.tight_layout()
plt.show()

# 差分
dlntbill = np.diff(lntbill)

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].plot(dlntbill)
axes[0, 0].set_title("Diff Log Data")
plot_acf(dlntbill, ax=axes[0, 1], title="ACF Diff Log")
plot_pacf(dlntbill, lags=30, ax=axes[1, 0], title="PACF Diff Log")
plt.tight_layout()
plt.show()

# 模型拟合 (AR6, MA6, ARMA6,6)
print("Fitting AR(6)...")
d3 = ARIMA(dlntbill, order=(6, 0, 0)).fit()
print(f"AR(6) AIC: {d3.aic}")
d3.plot_diagnostics(figsize=(10,8))
plt.show()

print("Fitting MA(6)...")
d4 = ARIMA(dlntbill, order=(0, 0, 6)).fit()
print(f"MA(6) AIC: {d4.aic}")

print("Fitting ARMA(6,6)...")
# 注意: 高阶 ARMA 可能收敛较慢
d5 = ARIMA(dlntbill, order=(6, 0, 6)).fit()
print(f"ARMA(6,6) AIC: {d5.aic}")


# --- 预测 ---
# 使用前 456 天 (Python index 0:456)
# R code uses 1:455 of differenced data (which corresponds to time up to 456)
train_diff = dlntbill[:455] 
fit_pred = ARIMA(train_diff, order=(6, 0, 0)).fit()
Y_pred = fit_pred.forecast(steps=6)

# 手动还原差分 (Forecast-1)
tfore = np.zeros(6)
last_real_val = ttbill[455] # Day 456
# Step 1
tfore[0] = np.exp(Y_pred[0]) * last_real_val
# Step 2-6
for i in range(1, 6):
    tfore[i] = np.exp(Y_pred[i]) * tfore[i-1]

# 使用 ARIMA(6,1,0) 直接在 Log 数据上拟合 (Forecast-2)
# 这会自动处理差分还原
train_log = lntbill[:456]
fit2 = ARIMA(train_log, order=(6, 1, 0)).fit()
# 这里的 forecast 已经是 log scale 的 level 值，不需要累乘，只需要 exp
tfore2_log = fit2.forecast(steps=6)
tfore2 = np.exp(tfore2_log)

# 绘图比较
actual = ttbill[456:462]
plt.figure(figsize=(8, 4))
plt.plot(range(457, 463), actual, label="Actual", linestyle='-')
plt.plot(range(457, 463), tfore, label="Forecast-1 (Manual)", linestyle='--')
plt.plot(range(457, 463), tfore2, label="Forecast-2 (Integrated)", linestyle=':')
plt.legend()
plt.title("Forecast Comparison")
plt.show()

# 预测区间 (Prediction Intervals)
# Python statsmodels get_forecast() 用于获取区间
forecast_res = fit2.get_forecast(steps=6)
fore_mean = np.exp(forecast_res.predicted_mean)
conf_int = forecast_res.conf_int(alpha=0.05) # 95%
lower = np.exp(conf_int[:, 0])
upper = np.exp(conf_int[:, 1])

# 绘制包含历史数据的图
plt.figure(figsize=(10, 5))
# 为了看清楚，只画最后50个点
plt.plot(np.arange(400, 456), ttbill[400:456], color='black', label='History')
plt.plot(np.arange(456, 462), actual, color='black', linestyle='-', label='Actual Future')
plt.plot(np.arange(456, 462), fore_mean, color='red', label='Forecast')
plt.plot(np.arange(456, 462), lower, color='green', linestyle='--', label='Lower 95%')
plt.plot(np.arange(456, 462), upper, color='green', linestyle='--', label='Upper 95%')
plt.legend()
plt.title("Forecast with Prediction Intervals")
plt.show()
print("\n")


# ==========================================
# 3. Accident Death Example
# ==========================================
print("--- Accident Death Example ---")

# --- 数据加载 ---
try:
    # accdeaths = pd.read_csv("accdeaths.dat", header=None).values.flatten()
    # 模拟季节性数据
    t = np.arange(72)
    accdeaths = 8000 + 50 * t + 2000 * np.sin(2 * np.pi * t / 12) + np.random.normal(0, 200, 72)
except:
    accdeaths = np.array([])

# 划分测试集 (最后 12 个月)
train_acc = accdeaths[:60]
test_acc = accdeaths[60:72]

# 创建 Pandas Series 以便 STL 识别频率
# R frequency=12 -> Pandas period
ts_data = pd.Series(train_acc, index=pd.date_range(start='1973-01-01', periods=60, freq='M'))

# 绘图和 ACF/PACF
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].plot(train_acc)
axes[0, 0].set_title("Accidental Deaths")
plot_acf(train_acc, lags=20, ax=axes[0, 1])
plot_pacf(train_acc, lags=20, ax=axes[1, 0])
plt.tight_layout()
plt.show()

# STL 分解
# R: stl(x, s.window="periodic")
res = STL(ts_data, seasonal=13, period=12).fit() # seasonal必须是奇数
res.plot()
plt.show()

# 提取分量
trend = res.trend
seasonal = res.seasonal
resid = res.resid # y in R code (Noise)

# ARMA Model Fitting on Noise
# R: auto.arima(y, ic="aic", ...)
# Python equivalent: pmdarima.auto_arima
print("Auto ARIMA on residuals...")
arma_fit = pm.auto_arima(resid, 
                         max_p=3, max_q=3, 
                         stepwise=False, 
                         information_criterion='aic',
                         seasonal=False) # 我们已经移除了季节性
print(arma_fit.summary())

# 诊断图
arma_fit.plot_diagnostics(figsize=(10, 8))
plt.show()

# 预测残差
pred_resid, conf_int_resid = arma_fit.predict(n_periods=12, return_conf_int=True)

# 重构预测 (Reconstruct Forecast)
# 1. 趋势推断 (线性外推)
# R: inc = trend[60] - trend[59]
last_trend = trend.iloc[-1]
prev_trend = trend.iloc[-2]
inc = last_trend - prev_trend
# Forecast trend for next 12 steps
fore_trend = last_trend + inc * np.arange(1, 13)

# 2. 季节性 (取过去12个月的季节性作为未来预测)
# R: seasonal[1:12] (Assuming strict periodic)
# 在 STL 中，最后 12 个月的季节性分量
fore_seasonal = seasonal.iloc[-12:].values 

# 3. 总预测
fore = fore_trend + fore_seasonal + pred_resid

# 4. 置信区间 (R code roughly adds 1.96*se to the total forecast)
# 这里我们使用残差预测的置信区间宽度
lower_bound = fore_trend + fore_seasonal + conf_int_resid[:, 0]
upper_bound = fore_trend + fore_seasonal + conf_int_resid[:, 1]

# 结果可视化
plt.figure(figsize=(10, 6))
# 绘制测试集真实值
plt.plot(np.arange(1, 13), test_acc, 'k-', label='Actual (1978)')
# 绘制预测值
plt.plot(np.arange(1, 13), fore, 'r-', label='Forecast')
# 绘制区间
plt.plot(np.arange(1, 13), upper_bound, 'b--', label='Upper 95%')
plt.plot(np.arange(1, 13), lower_bound, 'b--', label='Lower 95%')
plt.title("Forecast Reconstruction (Trend + Seasonal + ARMA resid)")
plt.legend()
plt.show()

# 将所有部分画在一起
plt.figure(figsize=(12, 6))
full_history = np.concatenate([train_acc, test_acc])
full_forecast = np.concatenate([train_acc, fore]) # 前面用真实值填充以便连线
full_upper = np.concatenate([train_acc, upper_bound])
full_lower = np.concatenate([train_acc, lower_bound])

plt.plot(full_history, 'k-', label='Data')
plt.plot(range(60, 72), fore, 'r-', label='Forecast')
plt.fill_between(range(60, 72), lower_bound, upper_bound, color='blue', alpha=0.2)
plt.axvline(x=60, color='gray', linestyle='--')
plt.title("Full Series with Forecast")
plt.show()