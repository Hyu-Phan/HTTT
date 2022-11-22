import pandas as pd

data = pd.read_excel("Case.xlsx", sheet_name=[
                     'Case', 'Lỗi', 'Tiêu chí'], index_col=0)
data2 = pd.read_excel("Độ tương đồng.xlsx", sheet_name=['Hoạt động', 'Tình trạng', 'Nhiệt độ', 'Đèn báo lỗi, bảng hiển thị',
                                                        'Quạt dàn lạnh', 'Quạt dàn nóng', 'Cục nóng', 'Ống đồng', 'Mùi', 'Tín hiệu remote'], index_col=0)

signals = ['HD02', 'TT02', 'ND03', 'DB02',
           'QL02', 'QN01', 'CN01', 'OD01', 'M01', 'TH01']

cases = data['Case']
errors = data['Lỗi']
weights = data['Tiêu chí']
max_probability = 0
id = 0

dict_signal = {
    'HD': 'Hoạt động',
    'TT': 'Tình trạng',
    'ND': 'Nhiệt độ',
    'DB': 'Đèn báo lỗi, bảng hiển thị',
    'QL': 'Quạt dàn lạnh',
    'QN': 'Quạt dàn nóng',
    'CN': 'Cục nóng',
    'OD': 'Ống đồng',
    'M': 'Mùi',
    'TH': 'Tín hiệu remote'
}

for index, case in cases.iterrows():
    sum1 = sum2 = 0
    for signal_code in signals:
        code = signal_code
        signal = signal_code[:-2]
        signal = dict_signal[signal]
        weight = weights.loc[signal, 'Trọng số']
        similarity = data2[signal].loc[code, case[signal]]
        sum1 +=  weight*similarity
        sum2 +=  weight

    probability = sum1/sum2
    if(max_probability < probability):
        max_probability = probability
        id = index

print(max_probability)
print(errors['Lỗi'][cases.loc[11, 'Lỗi']])
print(errors['Khắc phục'][cases.loc[11, 'Lỗi']])
