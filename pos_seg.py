from defi import pat_Seg
from defi import pat_Pos
from defi import Av2_log
from defi import pos_seg_path


def get_pos_seg():
    with open(Av2_log, 'r', encoding='utf-8') as f:
        lir = f.readlines()
    with open(pos_seg_path, 'w', encoding='utf-8') as file:
        for i in range(len(lir)):
            m = pat_Pos.findall(lir[i])
            n = pat_Seg.findall(lir[i])
            if m or n:
                file.write(lir[i])
                file.write('\n')


if __name__ == '__main__':
    get_pos_seg()