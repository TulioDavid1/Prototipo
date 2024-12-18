import numpy as np
import win32gui, win32ui, win32con


class WindowCapture:

    # Propriedades da classe
    w = 0  # Largura da janela
    h = 0  # Altura da janela
    hwnd = None  # Handle (identificador) da janela
    cropped_x = 0  # Recorte na coordenada X (para bordas)
    cropped_y = 0  # Recorte na coordenada Y (para barra de título)
    offset_x = 0  # Deslocamento X para coordenadas da tela
    offset_y = 0  # Deslocamento Y para coordenadas da tela

    # Construtor da classe
    def __init__(self, window_name="", size=(818, 640), origin=(0, 0)):
        self.size = size  # Tamanho da área de captura
        self.origin = origin  # Origem da captura na tela
        self.hwnd = None  # Handle da janela
        self.window_name = window_name  # Nome da janela

        if window_name == "":
            # Captura de tela inteira
            self.hwnd = None
            self.w = self.size[0]  # Largura da captura
            self.h = self.size[1]  # Altura da captura
        else:
            # Encontrar o handle da janela com base no nome
            print("window_name", window_name)
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))
            
            # Obter o tamanho da janela
            window_rect = win32gui.GetWindowRect(self.hwnd)
            print("window_rect", window_rect)
            self.w = window_rect[2] - window_rect[0]
            self.h = window_rect[3] - window_rect[1]
            print("self.w", self.w)

        # Ajustar para bordas e barra de título
        border_pixels = 8  # Largura das bordas
        titlebar_pixels = 31  # Altura da barra de título
        if not window_name == "":
            self.w = self.w - (border_pixels * 2)
            self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # Configurar deslocamentos para traduzir coordenadas
        if window_name == "":
            self.offset_x = self.size[0] + self.cropped_x
            self.offset_y = self.size[1] + self.cropped_y
        else:
            self.offset_x = window_rect[0] + self.cropped_x
            self.offset_y = window_rect[1] + self.cropped_y

    # Método para capturar a tela
    def get_screenshot(self):
        # Obter o contexto gráfico da janela
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)

        # Copiar dados da tela/área da janela para o bitmap
        if self.window_name == "":
            cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.origin[0], self.origin[1]), win32con.SRCCOPY)
        else:
            cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        # Converter os dados brutos em um formato que o OpenCV pode ler
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # Liberar recursos do sistema
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # Remover o canal alfa, necessário para algumas operações do OpenCV
        img = img[..., :3]

        # Tornar a imagem contígua em memória para evitar erros
        img = np.ascontiguousarray(img)

        return img

    # Listar os nomes das janelas abertas no sistema
    def list_window_names(self):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    # Traduzir uma posição de pixel da imagem para a posição na tela
    # pos = (x, y)
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)
