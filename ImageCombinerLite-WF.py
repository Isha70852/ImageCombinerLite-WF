import PySimpleGUI as sg
import os 
from PIL import Image
import webbrowser

# 合併
# 用來合併的圖片列表
filelist = []
# 要儲存的位置
filepath = ""

# 分割
# 來源圖片
filepath2 = ""
filepath2_name = []
# 要儲存的位置
filepath2_folder = ""

def ChooseFilePath():
    # 來源資料夾
    filepath = sg.popup_get_folder("選擇資料夾",no_window= True)
    if not filepath:
        return
    window['-FILEPATHTEXT-'].update(filepath)
    filelist = []
    for f in os.listdir(filepath):
        if f.lower().endswith((".jpg", ".png")):
            filelist.append(os.path.join(filepath, f))
    return filelist

def Combine(filelist , filepath):
    img = []
    columnNumber = 0 #現在在第幾行
    rowNumber = 0 #現在在第幾列
    column = int(values['-COLUMN-'])
    row = int(values['-ROW-'])
    for i in filelist:
        img.append(Image.open(i))
    
    width = img[0].size[0] * column
    height = img[0].size[1] * row
    columnSize = width / column
    rowSize = height / row
    blankCanvas = Image.new(mode = "RGBA", size = (width, height), color = (255, 255, 255,255))
    for index,  i in enumerate(img):
        if int((index + 1) % column) == 0:
            blankCanvas.paste(i, box = (int(columnNumber * columnSize),  int(rowNumber * rowSize)))
            rowNumber += 1 #整除rowNumber +1
            columnNumber = 0 #columnNumber 歸0
        else:
            blankCanvas.paste(i, box = (int(columnNumber * columnSize),  int(rowNumber * rowSize)))
            columnNumber +=1
            
    # 儲存
    if filepath.endswith(".jpg"):
        saveBlankImage = Image.new(mode="RGB",size=blankCanvas.size, color = (255,255,255))
        saveBlankImage.paste(blankCanvas, (0,0), blankCanvas)
        saveBlankImage.save(filepath)
        sg.popup("已儲存")
    elif filepath.endswith(".png"):
        blankCanvas.save(filepath)
        sg.popup("已儲存")
    else:
        sg.popup("不支援的格式")

def ChooseFilePath2():
    filepath = sg.popup_get_file("選擇檔案",default_extension='.png',file_types=(("PNG",".png"),("JPG",".jpg")),no_window= True)
    if not filepath:
        return
    filepathName = filepath.split('/')[-1].split('.')
    window['-FILEPATH2TEXT-'].update(filepath)
    return filepath , filepathName

def Split(filepath2, filepath2_folder, filepath2_name):
    img = Image.open(filepath2)
    split_img = []
    column = int(values['-COLUMN2-'])
    row = int(values['-ROW2-'])

    width = img.size[0]
    height = img.size[1]
    columnSize = width / column
    rowSize = height / row
    
    for i in range(0,column):
        for j in range(0,row):
            split_img.append(img.crop((i * columnSize, j * rowSize, (i+1) * columnSize, (j+1) * rowSize))) 
            
    for index, i in enumerate(split_img):
        i.save(os.path.join(filepath2_folder, filepath2_name[0]) + "_split_" +  f'{index}' + '.' +  filepath2_name[1]) 
    
    sg.popup("已儲存")

sg.theme("Dark")

Combinelayout = [
                [sg.Button("選擇資料夾",key = '-FILEPATH-'), sg.Text("", key = '-FILEPATHTEXT-')],
                [sg.Input("", size = (20,20), key = '-COLUMN-'), sg.Text("行"), sg.Input("" , size = (20,20), key = '-ROW-'), sg.Text("列")],
                [sg.Button("另存新檔", key = '-OUTPUTPATH-'), sg.Text("", key = '-OUTPUTPATHTEXT-'),sg.Push(), sg.Button("合併", key = '-COMBINE-')]
                
    ]

Splilayout = [
            [sg.Button("選擇檔案", key ='-FILEPATH2-'), sg.Text("", key = '-FILEPATH2TEXT-')],
            [sg.Input("", size = (20,20), key = '-COLUMN2-'), sg.Text("行"), sg.Input("" , size = (20,20), key = '-ROW2-'), sg.Text("列")],
            [sg.Button("選擇輸出資料夾", key = '-OUTPUTPATH2-'), sg.Text("", key = '-OUTPUTPATH2TEXT-'),sg.Push(), sg.Button("分割", key = '-SPLIT-')]
    ]

Aboutlayout =[
    [sg.Push(),sg.Text("ImageCombinerLite-WF"), sg.Push()],
    [sg.Text("ImageCombinerLite-WF is a free, lightweight app for\ncombining images and splitting image.\n\nPowered by PySimpleGUI and Pillow.")],
    [sg.Text("WizardForest."), sg.Text("Learn more.",text_color= 'lightblue', enable_events= True, key = '-ABOUT-')]
    ]



layout = [[sg.TabGroup([[sg.Tab("合併圖片", Combinelayout), sg.Tab("分割圖片", Splilayout), sg.Tab("關於", Aboutlayout)]])]]

window = sg.Window('ImageCombinerLite-WF', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == '-FILEPATH-':
        filelist =  ChooseFilePath()
    if event == '-OUTPUTPATH-':
        filepath = sg.popup_get_file("另存新檔",default_extension='.png',file_types=(("PNG",".png"),("JPG",".jpg")),  save_as=True , no_window= True)
        window['-OUTPUTPATHTEXT-'].update(filepath)
    if event == '-COMBINE-':
        Combine(filelist, filepath)
    if event == '-FILEPATH2-':
        filepath2, filepath2_name = ChooseFilePath2()
        
    if event == '-OUTPUTPATH2-':
        filepath2_folder = sg.popup_get_folder("選擇資料夾",no_window= True)
        window['-OUTPUTPATH2TEXT-'].update(filepath2_folder)
    if event == '-SPLIT-':
        Split(filepath2, filepath2_folder, filepath2_name)
    if event == '-ABOUT-':
        webbrowser.open("https://home.gamer.com.tw/artwork.php?sn=5448028")
window.close() 