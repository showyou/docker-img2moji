from PIL import Image, ImageDraw, ImageFont
import sys

XSIZE = 128
YSIZE = 128

# 与えた画像を、グレースケールのリストに変換する関数（白＝1、灰＝0.5、黒＝0）
# 元がカラー画像でも対応出来るようにしている
def img2graylist(input_img):
  #幅と高さを取得する
  img_width, img_height = input_img.size
  print('幅　: ', img_width)
  print('高さ: ', img_height)

  #最終的に出力する二次元リスト
  result_graylist = []
  for y in range(0, img_height, 1):
    # １行ごとのテンポラリリスト
    tmp_graylist=[]
    for x in range(0, img_width, 1):
      # 1ピクセルのデータ（RGB値）を取得
      #(20, 16, 17, 255)のように４つのデータが取れる⇒3つに絞って使う
      r,g,b, = input_img.getpixel((x,y))[0:3]

      #RGB値の平均＝グレースケールを求める
      g = (r + g + b)/3
      tmp_graylist.append(g)
    #１行終わるごとにテンポラリリストを最終出力に追加
    result_graylist.append(tmp_graylist)
  return result_graylist

# 与えたグレイリストを、白＝1、黒＝0のリストに変換する関数
# 黒が多い画像⇒全て黒、や、色の薄い画像⇒全て白、にならないように、
# 閾値として、平均値を取得した後で、その閾値との大小で判定する
# よって、薄い画像が全部白に、濃い画像が全部黒に、などはならない
import numpy as np
def graylist2wblist(input_graylist):

  #与えられた二次元配列の値の平均値を求める(npを使っても良いが)
  gray_sum_list = []
  for tmp_graylist in input_graylist:
    gray_sum_list.append( sum(tmp_graylist)/len(tmp_graylist) )
  gray_ave = sum(gray_sum_list)/len(gray_sum_list) 
  print("灰色平均値： ", gray_ave)

  # 最終的に出力する二次元の白黒リスト
  result_wblist = []
  for tmp_graylist in input_graylist:
    tmp_wblist = []
    for tmp_gray_val in tmp_graylist:
      #閾値と比べて大きいか小さいかによって１か０を追加
      if tmp_gray_val >= gray_ave:
        tmp_wblist.append(1)
      else:
        tmp_wblist.append(0)
    result_wblist.append(tmp_wblist)

  return result_wblist
  

## 与えられた文字列を、画像にする関数
## １文字あたりのサイズ＆縦横の文字数も引数で指定
def str2img(input_str, yoko_mojisuu, tate_mojisuu, moji_size):
  # 真っ白な背景画像を生成する
  # 横（縦）幅 ＝ 文字サイズ× 横（縦）文字数
  img  = Image.new('RGBA', (moji_size * yoko_mojisuu , moji_size * tate_mojisuu), 'white')
  # 背景画像上に描画を行う
  draw = ImageDraw.Draw(img)

  # フォントの読み込みを行う。（環境によって異なる）
  myfont = ImageFont.truetype("fonts-japanese-gothic.ttf    /usr/share/fonts/truetype/fonts-japanese-gothic.ttf", moji_size)

  # 文字を書く。基本は以下で済むが、今回は１文字ずつ記入
  # draw.text((0, 0), input_str , fill=(0, 0, 0), font = myfont)
  # ※備考：１文字ずつ記入の場合、半角と全角を区別しないといけなくなる
  # （今回は全角前提とする）
  # fillは、文字の色をRBG形式で指定するもの。今回は黒なので0,0,0固定
  # 縦横のサイズに合せて１文字ずつ描画
  yoko_count = 0
  tate_count = 0
  for char in input_str:
    #縦の文字数の許容量を途中でオーバーしてしまった場合は終了
    if tate_count >= tate_mojisuu:
      break
    #所定の位置に1文字ずつ描画
    draw.text( ( yoko_count * moji_size, tate_count * moji_size ), char, fill=(0, 0, 0), font = myfont)
    yoko_count +=1
    if yoko_count >= yoko_mojisuu:
      yoko_count =  0
      tate_count += 1

  return img


#与えられた2次元文字列リストをプリントする関数（pprint的なもの）
#（※最終出力時には使わないが、途中経過を見る用途）
def print2Dcharlist(charlist):
  for tmp_charlist in charlist:
    for char in tmp_charlist:
      #改行無しで出力
      print(char, end="")
    #1行終わるごとに改行
    print()


# ToDo: resizeの128を変数にする
def load_image(filename):
  print(filename)
  img = Image.open(filename)
  img = img.resize((XSIZE,YSIZE))
  return img


def img2charlist(image_name):
  img = load_image(image_name)
  graylist = img2graylist(img)
  wblist = graylist2wblist(graylist)

  print2Dcharlist(wblist)


# 文字列を一文字ずつ取り出すジェネレータ。半無限ループにより繰り返し
def infinity_gen_str(str):
  for a in range(1000000000):
    for s in str:
        yield s


# 以下のように使う
# 定義：gen_str =  infinity_gen_str("表示したい文字列")
# 使用：next(gen_str)
# これで、使用するたびに１文字ずつ出力される


# 白黒リストの、白黒の部分を文字列で埋め尽くした二次元リストを返す
# 白＝soto_strで埋める。黒＝nakami_strで埋める。
def wblist2wbcharlist(input_wblist, nakami_str, soto_str):
  # １文字ずつ出力できるジェネレータの生成
  gen_nakami_str =  infinity_gen_str(nakami_str)
  gen_soto_str =  infinity_gen_str(soto_str)

  # 最終的に出力する二次元の白黒リスト
  result_wbcharlist = []
  for tmp_wblist in input_wblist:
    tmp_wbcharlist = []
    for tmp_wb_val in tmp_wblist:
      # 値が１か０かによって、文字列を入れていく
      # ※空白と等幅になる文字＆フォントでやることが望ましい
      if tmp_wb_val == 1:
        # 1が白
        # 空白固定ならコレでも同じ ⇒ tmp_wbcharlist.append( "　" )
        tmp_wbcharlist.append( next(gen_soto_str))
      else:
        # 0が黒
        tmp_wbcharlist.append( next(gen_nakami_str) )

    result_wbcharlist.append(tmp_wbcharlist)

  return result_wbcharlist


def img2moji(image_name, after_image_name, moji):
  img = load_image(image_name)
  graylist = img2graylist(img)
  wblist = graylist2wblist(graylist)
  #print2Dcharlist(wblist)

  # 今回は↑の外枠で「」のフレーム（０１）を作り、
  # ↓の指定で、中身を「」の文字列で埋める
  wbcharlist = wblist2wbcharlist(wblist, moji,"　")
  print2Dcharlist(wbcharlist)


  all_str = ""
  for tmp_list in wbcharlist:
    for char in tmp_list:
      all_str += char

  moji_size = 1
  final_moji_size = 10
  img1 = str2img(all_str, XSIZE*moji_size, YSIZE*moji_size, final_moji_size)
  img1.save(after_image_name)
  print("save done.")


if __name__ == '__main__':
  image_name = sys.argv[1]
  after_image_name = sys.argv[2]
  moji = sys.argv[3]
  img2moji(image_name, after_image_name, moji)