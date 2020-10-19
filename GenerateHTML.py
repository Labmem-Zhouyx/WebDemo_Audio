import numpy as np
import random

def generate_html(title, description, experiement_name, column_name, text_sample, audio_sample, audio_type, is_random):
    '''
    :param title: 网页标题
    :param description: 网页demo描述，可以有多条，默认居中。例如：论文名称、作者、评测注意事项等，
    :param experiement_name: 实验组名称, shape=N。例如：['exp1', 'exp2', 'exp3', ... ]
    :param column_name: 每组实验列名称，shape=(N,c)。例如：[['col1_1','col1_2',], ['col2_1', 'col2_2', 'col2_3', ], ... ]
    :param text_sample:每组实验每个样例的文本，shape=(N,k)。
            例如[['sentence0','sentence1','sentence2', ...],['sentence51','sentence53','sentence55', ...], ...]
    :param audio_sample: 每组实验每个样例音频编号，根据该值索引wavs/audio_*/中选取的*.wav文件，shape=(N,k)。例如：[[0,1,2,...], [51,53,55,...], ... ]
    :param audio_type: 音频类别，每句话有t个平行音频，根据该值选取wavs/的audio目录，shape=(N,t)。例如[[0,1,2],[0,1], ... ]
    :param is_random: 每组实验的每一行t个音频是否随机打乱，一般测评时需要随机，展示不用。例如：[True,False, ...]
    :return:
        生成一个html文件，显示demo网页
        生成一个xls表格，显示打乱结果，若不打乱则默认是顺序，shape=(N,k,t）
    '''
    html_file = []
    html_file.append('<!DOCTYPE html>')
    html_file.append('<html>')
    #设置网页标题
    html_file.append('<head><title>' + title + '</title></head>')
    html_file.append('<body>')
    #设置网页说明
    for des in description:
        html_file.append('<h2><center>' + des + '</center></h2>')
        
    #设置第exp_index组实验
    reorder = []
    for exp_index in range(len(experiement_name)):
        html_file.append('<h2>' + experiement_name[exp_index] + '</h2>')
        html_file.append('<table style="width:100%">')
        html_file.append('<tr>')
        for col in column_name[exp_index]:
            html_file.append('<th>' + col + '</th>')
        html_file.append('</tr>')
        html_file.append('</table>')
        if is_random[exp_index]:
            # 将不同模型类别音频随机打乱
            reorder_list = []
            for i in range(len(audio_sample[exp_index])):
                audio_type_deep_copy = audio_type[exp_index][:]
                random.shuffle(audio_type_deep_copy)
                reorder_list.append(audio_type_deep_copy)
            reorder.append(reorder_list)
        else:
            reorder.append([audio_type[exp_index] for i in range(len(audio_sample[exp_index]))])
        for sample_index in range(len(audio_sample[exp_index])):
            html_file.append('<p>' + text_sample[exp_index][sample_index] + '</p>')
            html_file.append('<table style="width:100%">')
            html_file.append('<tr>')
            html_file.append('<th>' + str(sample_index) + '</th>')
            for type_index in reorder[exp_index][sample_index]:
                html_file.append('<th>')
                html_file.append('<audio controls style="width: 250px;">')
                #若需要，在此处修改音频文件名格式
                html_file.append('<source src="./wavs/audio_' + str(type_index) + '/wav-batch_' + str(audio_sample[exp_index][sample_index]) + '_sentence_0-linear.wav" type="audio/mpeg">')
                html_file.append('Your browser does not support the audio element.')
                html_file.append('</audio>')
                html_file.append('</th>')
            html_file.append('</tr>')
            html_file.append('</table>')
    html_file.append('</body>')
    html_file.append('</html>')


    #输出html文件
    html_file_output = '\n'.join(html_file)
    with open('demo_index.html', 'w') as f:
        f.write(html_file_output)

    #输出打乱后的顺序excel文件
    with open('table_NewOrder.xls', 'w') as f:
        for exp_index in range(len(reorder)):
            f.write(experiement_name[exp_index] + '\n')
            for sample_index in range(len(reorder[exp_index])):
                for audiotype in reorder[exp_index][sample_index]:
                    f.write(str(audiotype)+'\t')
                f.write('\n')
            f.write('\n')

    print(html_file_output)
    print(reorder)


#使用前设置好相关参数，将每个模型的音频文件放到wavs下的建立的'audio_*'目录中，可根据实际音频文件名修改格式，运行得到demo_index.html
title = 'Syntactic Tree TTS'
description = ['Demo for baseline(WRF), proposed_1(BiRNN with BNM), proposed_2(BiRNN without BNM)', 'The order of audio in every sample is RANDOM']
experiement_name = ['Reference for MOS', 'MOS','Reference for ABTest', 'ABTest']
column_name = [['A', 'B'], ['Sample 0','Sample 1'],['A','B'], ['Sample 0','Sample 1']]
audio_sample = [[68,69], [70,71,72,73,74,75],[3], [0,1,2,4]]
text_sample = []
with open('./wavs/sentences.txt','r', encoding='utf-8') as f:
    for line in f.readlines():
        text_sample.append(line.strip())
text_sample = [list(np.array(text_sample)[sub_audio_sample]) for sub_audio_sample in audio_sample]
audio_type = [[0,1], [0,1], [1,2], [1,2]]
is_random = [False, True, False, True]

generate_html(title, description, experiement_name, column_name, text_sample, audio_sample, audio_type, is_random)

