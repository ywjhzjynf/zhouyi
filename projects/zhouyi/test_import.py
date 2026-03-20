import sys
sys.path.insert(0, '.')
from mobile import divine

r = divine('coin')
print('导入成功！')
print(f'卦名：{r["hexagram"]}')
print(f'测试状态：{"PASS" if r["success"] else "FAIL"}')
