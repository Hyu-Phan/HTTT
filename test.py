
import yaml
import pandas as pd

data = pd.read_excel("Case.xlsx", sheet_name=[
                     'Case', 'Lỗi', 'Tiêu chí'], index_col=0)
data2 = pd.read_excel("Độ tương đồng.xlsx", sheet_name=['Hoạt động', 'Tình trạng', 'Nhiệt độ', 'Đèn báo lỗi, bảng hiển thị',
                                                        'Quạt dàn lạnh', 'Quạt dàn nóng', 'Cục nóng', 'Ống đồng', 'Mùi', 'Tín hiệu remote'], index_col=0)


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


with open('question2.yml', 'r', encoding="utf8") as f:
    doc = yaml.load(f, Loader=yaml.FullLoader)
doc = dict(doc)
signals = []

print('Hệ thống: Bạn cần tư vấn về vấn đề gì?')

for key in doc.keys():
    print('Hệ thống:', doc[key]['question'])
    for option in doc[key]['options']:
        print(option)

    ops = input('Người dùng: ').split(',')
    signal = ''
    for i, op in enumerate(ops):
        code = doc[key]['code']
        signal += f'{code}%02d' % int(op)
        if i != len(ops) - 1: 
            signal += ', '
    signals.append((code, signal))

print(signals)

cases = data['Case']
errors = data['Lỗi']
weights = data['Tiêu chí']
max_probability = 0
id = 0

for index, case in cases.iterrows():
    sum1 = sum2 = 0
    for signal_code in signals:
        code = signal_code[1]
        signal = dict_signal[signal_code[0]]
        weight = weights.loc[signal, 'Trọng số']
        similarity = data2[signal].loc[code, case[signal]]
        sum1 += weight*similarity
        sum2 += weight

    probability = sum1/sum2
    if (max_probability < probability):
        max_probability = probability
        id = index

print(max_probability)
print(errors['Lỗi'][cases.loc[id, 'Lỗi']])
print(errors['Khắc phục'][cases.loc[id, 'Lỗi']])
