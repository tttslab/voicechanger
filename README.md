# voicechanger
The program takes two sound files file1.wav and file2.wav.
It extracts sound source information (higher quefrency component)
from the first input, and filter information (lower quefrency component)
from the second input. 
Then it synthesizes output by combining them.

To run the program, python3 is required.
Using anaconda is convenient.
I have tested the program on windows10 and Linux.
Input wav files must be Monaural/16kHz/16bit PCM.

Usage:
python voicechanger.py samplewav\sawtooth100hz.wav samplewav\toukoudai.wav out.wav

Note: the sample wav file neorock38.wav is based on a free sound material by 魔王魂.

2つの音声ファイルfile1.wav, file2.wavを受け取り、初めの音声から
音源情報（高ケプストラム成分）を抽出、2番目の音声からスペクトラム
包絡（低ケプストラム成分）を抽出する。そして、それらを再合成した
音声を出力する。

準備：
python3をインストール
anacondaを用いるのが便利
windows10とlinuxで動作を確認
入力音声ファイルはMonaural/16kHz/16bit PCM形式で用意してください
サンプル音声ファイルのうちneorock38.wavは、魔王魂によるフリー音楽素材をもとにファイル形式を変換したものです

使用例：
python voicechanger.py samplewav\sawtooth100hz.wav samplewav\toukoudai.wav out.wav


# Written by Takahiro Shinozaki
# Tokyo Institute of Technology
# 2017/2/15
