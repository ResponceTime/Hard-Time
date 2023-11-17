#importa as bibliotecas necessarias
import pygame as pg
import random
import os
from pygame import Rect

#Funções
def carregar_pergunta():
    global resposta, numero_de_perguntas, nivel, quantidade_de_perguntas, alternativa1, alternativa2, alternativa3, alternativa4, dica, str_num_pergunta, \
        musica, nivel_atual_txt, fonte_bauhs, fonte_courbd, tempo_max
    arquivo_do_nivel_atual = nivel_atual_txt
    fonte_do_numero_da_pergunta = pg.font.Font(fonte_bauhs, 36)
    fonte_das_perguntas_e_alternativas = pg.font.Font(fonte_courbd, 29)

    str_num_pergunta = str(numero_de_perguntas+1)
    texto_renderizado = fonte_do_numero_da_pergunta.render(str_num_pergunta, True, (255, 255, 255))
    screen.blit(texto_renderizado, (203-10*len(str(numero_de_perguntas+1))+10, 126))

    if numero_de_perguntas == 0:
      num = 0
    else:
      num = (numero_de_perguntas*12)-1

    with open(arquivo_do_nivel_atual, 'r', encoding='utf-8') as contador_de_linhas:
        numero_de_linhas = len(contador_de_linhas.readlines())
        quantidade_de_perguntas = (numero_de_linhas)/12+1
        if nivel == 1:
            quantidade_de_perguntas_nivel1 = quantidade_de_perguntas
        if nivel == 2:
            quantidade_de_perguntas_nivel2 = quantidade_de_perguntas
        if nivel == 3:
            quantidade_de_perguntas_nivel3 = quantidade_de_perguntas

    with open(arquivo_do_nivel_atual, 'r', encoding='utf-8') as arquivo_linha_a_linha:
        for pergunta_atual in range(numero_de_linhas):
            linha = arquivo_linha_a_linha.readline()
            if not linha:
                break
            
            if pergunta_atual == num:
                #carregando pergunta linha1
                texto = fonte_das_perguntas_e_alternativas.render(linha.strip(), True, (255, 255, 255))
                screen.blit(texto, (255, 130))
            if pergunta_atual == num + 1:
                # carregando pergunta linha2
                texto = fonte_das_perguntas_e_alternativas.render(linha.strip(), True, (255, 255, 255))
                screen.blit(texto, (208, 180))
            if pergunta_atual == num + 2:
                # carregando pergunta linha3
                texto = fonte_das_perguntas_e_alternativas.render(linha.strip(), True, (255, 255, 255))
                screen.blit(texto, (208, 230))

            if pergunta_atual == num + 3:
                # carregando alternativa 1
                alternativa1 = linha.strip()
                texto = fonte_das_perguntas_e_alternativas.render(alternativa1, True, (255,255,255))
                screen.blit(texto, (175, 335))
            if pergunta_atual == num + 4:
                # carregando alternativa 2
                alternativa2 = linha.strip()
                texto = fonte_das_perguntas_e_alternativas.render(alternativa2, True, (255,255,255))
                screen.blit(texto, (175, 410))
            if pergunta_atual == num + 5:
                # carregando alternativa 3
                alternativa3 = linha.strip()
                texto = fonte_das_perguntas_e_alternativas.render(alternativa3, True, (255,255,255))
                screen.blit(texto, (175, 485))
            if pergunta_atual == num + 6:
                # carregando alternativa 4
                alternativa4 = linha.strip()
                texto = fonte_das_perguntas_e_alternativas.render(alternativa4, True, (255,255,255))
                screen.blit(texto, (175, 560))

            if pergunta_atual == num + 7:
                # carregando dica
                dica = linha.strip()
                texto = fonte_das_perguntas_e_alternativas.render(mostra_dica, True, (255,255,255))
                screen.blit(texto, (118, 631))

            if pergunta_atual == num + 8:
                # carregando tempo maximo
                tempo_max = linha.strip()

            if pergunta_atual == num + 9:
                # carregando resposta
                resposta = int(linha.strip())

    temporizador()

def carrega_configuracoes():
    global config_txt, volume, res, dicas_ativas, salvar_acertos
    arquivo = config_txt
    
    with open(arquivo, "r", encoding="utf-8") as arquivo_lido:
        numero_de_linhas = len(arquivo_lido.readlines())
        
        for _ in range(numero_de_linhas):
            linha = arquivo_lido.readline()
            
            if not linha:
                break
            if "volume:" in linha:
                volume = float(linha[7:len(linha)])
            if "dicas_ativas:" in linha:
                dicas_ativas = "True" in linha
            if "salvar_acertos:" in linha:
                salvar_acertos = "True" in linha
    
    
def salva_configuracoes():
    global config_txt, volume, res, dicas_ativas, salvar_acertos
    arquivo = config_txt
    
    with open(arquivo, "w", encoding="utf-8") as arquivo_para_editar:
        arquivo_para_editar.write("volume:"+str(volume))
        arquivo_para_editar.write("\n")
        arquivo_para_editar.write("dicas_ativas:"+str(dicas_ativas))
        arquivo_para_editar.write("\n")
        arquivo_para_editar.write("salvar_acertos:"+str(salvar_acertos))
        
        arquivo_para_editar.close()
        

def pontuacao():
    global salvar_acertos, fonte_courbd, nivel1_acertos, nivel2_acertos, nivel3_acertos, \
        quantidade_de_perguntas_nivel1, quantidade_de_perguntas_nivel2, quantidade_de_perguntas_nivel3

    fonte = pg.font.Font(fonte_courbd, 38)
    texto = fonte.render(f"{nivel1_acertos:02}/{quantidade_de_perguntas_nivel1:02}", True, (255, 255, 255))
    screen.blit(texto, (157, 357))

    texto = fonte.render(f"{nivel2_acertos:02}/{quantidade_de_perguntas_nivel2:02}", True, (255, 255, 255))
    screen.blit(texto, (600, 259))

    texto = fonte.render(f"{nivel3_acertos:02}/{quantidade_de_perguntas_nivel3:02}", True, (255, 255, 255))
    screen.blit(texto, (993, 315))


def acertou():
    global numero_de_perguntas, primeiro_falta_quinze, nivel, nivel1_acertos, nivel2_acertos, nivel3_acertos,\
         sons_channel, volume, minutos, segundos, timer_finalizado, minutos_max, segundos_max, acertos

    som_acerto.set_volume(volume)
    som_acerto.play()

    minutos = minutos_max
    segundos = segundos_max
    timer_finalizado = False
    primeiro_falta_quinze = True

    acertos += 1
    numero_de_perguntas += 1
    if nivel == 1:
        nivel1_acertos += 1
    if nivel == 2:
        nivel2_acertos += 1
    if nivel == 3:
        nivel3_acertos += 1


def errou():
    global numero_de_perguntas, volume, sons_channel, som_erro, timer_finalizado, \
        minutos, segundos, erros, primeiro_falta_quinze
    
    som_erro.set_volume(volume)
    som_erro.play()
    minutos = 1
    segundos = 30
    timer_finalizado = True
    primeiro_falta_quinze = True
    erros += 1
    numero_de_perguntas += 1


def carrega_acertos():
    global acerto_txt, nivel1_acertos, nivel2_acertos, nivel3_acertos
    arquivo = acerto_txt

    with open(arquivo, "r", encoding="utf-8") as arquivo_lido:
        linhas = arquivo_lido.readlines()
        
        for linha in linhas:
            
            if not linha:
                break
            if "nivel 1:" in linha:
                try:
                    nivel1_acertos = int(linha[8:len(linha)])
                except:
                    nivel1_acertos = 0
            if "nivel 2:" in linha:
                try:
                    nivel2_acertos = int(linha[8:len(linha)])
                except:
                    nivel2_acertos = 0
            if "nivel 3:" in linha:
                try:
                    nivel3_acertos = int(linha[8:len(linha)])
                except:
                    nivel3_acertos = 0

                

def salva_acertos():
    global acerto_txt
    arquivo = acerto_txt

    with open(arquivo, "w", encoding="utf-8") as arquivo_para_editar:
        if nivel1_acertos >= nivel1_acertos_antes:
            arquivo_para_editar.write("nivel 1:" + str(nivel1_acertos))
        else:
            arquivo_para_editar.write("nivel 1:" + str(nivel1_acertos_antes))

        arquivo_para_editar.write("\n")

        if nivel2_acertos >= nivel2_acertos_antes:
            arquivo_para_editar.write("nivel 2:" + str(nivel2_acertos))
        else:
            arquivo_para_editar.write("nivel 2:" + str(nivel2_acertos_antes))

        arquivo_para_editar.write("\n")

        if nivel3_acertos >= nivel3_acertos_antes:
            arquivo_para_editar.write("nivel 3:" + str(nivel3_acertos))
        else:
            arquivo_para_editar.write("nivel 3:" + str(nivel3_acertos_antes))

        arquivo_para_editar.close()


def verifica_o_volume():
    global volume, quero_mais_que_sete

    if volume < 0.1:
        volume = 0.0
    elif 0.1 < volume < 0.2:
        volume = 0.1
    elif 0.2 < volume < 0.3:
        volume = 0.2
    elif 0.3 < volume < 0.4:
        volume = 0.3
    elif 0.4 < volume < 0.5:
        volume = 0.4
    elif 0.5 < volume < 0.6:
        volume = 0.5
    elif 0.6 < volume < 0.7:
        volume = 0.6
    elif 0.7 < volume < 0.8:
        volume = 0.7
    elif 0.8 < volume < 0.9:
        volume = 0.8
    elif 0.9 < volume < 1.0:
        volume = 0.9
    elif volume > 1.0:
        volume = 1.0


    if quero_mais_que_sete:
        volume += 0.1
        if 0.8 < volume < 0.9:
            volume = 0.8
        elif 0.9 < volume < 1.0:
            volume = 0.9
        elif volume > 1.0:
            volume = 1.0


def temporizador():
    global screen, timer_finalizado, numero_de_perguntas, segundos, minutos, tempo_max, segundos_max, minutos_max, \
        mostra_dica, index_de_cauculo, fonte_ds_digital, acertos, erros, primeiro_falta_quinze, tempo_alarme
    
    minutos_max = int(tempo_max[0:tempo_max.find(":")])
    segundos_max = int(tempo_max[tempo_max.find(":")+1:len(tempo_max)])

    segundos_max = segundos_max + (5*acertos)//nivel
    
    segundos_max = segundos_max if segundos_max < 60 else segundos_max % 60
    minutos_max = minutos_max if segundos_max < 60 else segundos_max // 60
    
    if timer_finalizado:
        segundos = segundos_max
        minutos = minutos_max

    timer_finalizado = False
    
    pg.time.delay(1000)

    if segundos <= 0:
        segundos = 59
        minutos -= 1
        som_minuto_passado.play()
    else:
        segundos -= 1
    
    if minutos < minutos_max and segundos <= 15 and segundos % 2 == 1:
        cor_do_timer = (255, 0, 0)
        tempo_alarme.play()
    else:
        cor_do_timer = (255, 255, 255)

    fonte_timer = pg.font.Font(fonte_ds_digital, 38)
    texto_timer = fonte_timer.render(f"{minutos:02} : {segundos:02}", True, cor_do_timer)
    screen.blit(texto_timer, (1149 - 20 * len(f"{minutos:02} : {segundos:02}"), 38))

    if minutos < minutos_max and segundos <= 0:
        minutos = minutos_max
        segundos = segundos_max
        timer_finalizado = True
        mostra_dica = ""
        numero_de_perguntas += 1
        som_fim_do_tempo.play()


def defini_o_incone_aleatoriamente():
    global x_movimentavel, y_movimentavel, x_de_movimentacao, y_de_movimentacao, tupla_de_icones_img, \
        icone_atual, x_inicial, y_inicial, x_final, y_final, rotate, rodador, index

    index_do_icone = random.randint(0, 11)
    icone_atual = tupla_de_icones_img[index_do_icone]
    x = icone_atual.get_size()[0]
    y = icone_atual.get_size()[1]
    rodador = random.randrange(5, 20)

    index = random.randrange(0, 2)
    if index == 0:
        x_movimentavel = x *-1
        y_movimentavel = random.randrange(0, 720)
        x_de_movimentacao = random.randrange(10, 20)
        y_de_movimentacao = 0
    if index == 1:
        y_movimentavel = y *-1
        x_movimentavel = random.randrange(0, 1280)
        y_de_movimentacao = random.randrange(10, 20)
        x_de_movimentacao = 0


def movi_o_icone():
    global screen, x_movimentavel, y_movimentavel, x_de_movimentacao, y_de_movimentacao, tupla_de_icones_img, \
        icone_atual, fade_icone, x_inicial, y_inicial, x_final, y_final, rotate, index, rodador
    screen.blit(pg.transform.rotate(icone_atual, float(rotate)), (x_movimentavel, y_movimentavel))

    x_movimentavel += x_de_movimencacao
    y_movimentavel += y_de_movimencacao
    rotate += float(rodador)
    fade_icone -= random.randint(0, 15)
    if fade_icone < 0:
        fade_icone = 255
        defini_o_incone_aleatoriamente()

    if x_movimentavel > 1280 or y_movimentavel > 720:
        defini_o_incone_aleatoriamente()

    icone_atual.set_alpha(fade_icone)


#Fim das funções -------------------------------

# Variaveis OS para interpretar os arquivos com mais facilidade
pasta_do_codigo            = os.path.dirname(__file__)
pasta_arquivos             = os.path.join(pasta_do_codigo, "arquivos")

pasta_fontes               = os.path.join(pasta_arquivos, "fontes")
pasta_sons                 = os.path.join(pasta_arquivos, "sons")
pasta_perguntas            = os.path.join(pasta_arquivos, "perguntas")
pasta_imgs                 = os.path.join(pasta_arquivos, "imagens")
pasta_icones               = os.path.join(pasta_arquivos, "icones")

fonte_arial                = os.path.join(pasta_fontes, "arial.ttf")
fonte_bauhs                = os.path.join(pasta_fontes, "bauhs93.TTF")
fonte_courbd               = os.path.join(pasta_fontes, "courbd.ttf")
fonte_courbi               = os.path.join(pasta_fontes, "courbi.ttf")
fonte_couri                = os.path.join(pasta_fontes, "couri.ttf")
fonte_cour                 = os.path.join(pasta_fontes, "cour.ttf")
fonte_data_setenta         = os.path.join(pasta_fontes, "data_70_regular.otf")
fonte_ds_digital           = os.path.join(pasta_fontes, "ds_digib.TTF")

acerto_som_arquivo         = os.path.join(pasta_sons, "correto.mp3")
erro_som_arquivo           = os.path.join(pasta_sons, "incorreto.mp3")
tempo_som_arquivo          = os.path.join(pasta_sons, "tempo.mp3")
tempo_esgotado_arquivo     = os.path.join(pasta_sons, "tempo_esgotado.mp3")
passou_um_minuto_arquivo   = os.path.join(pasta_sons, "a_minute_has_go.mp3")
amphitruo                  = os.path.join(pasta_sons, "amphitruo.mp3")
amfitras                   = os.path.join(pasta_sons, "amfitras.mp3")
reliquia                   = os.path.join(pasta_sons, "reliquia.mp3")
oito_bits                  = os.path.join(pasta_sons, "oito_bits.mp3")
escolha_errada             = os.path.join(pasta_sons, "escolha_errada.mp3")
lista_de_musicas = amphitruo, amfitras, reliquia, oito_bits, escolha_errada

config_txt                 = os.path.join(pasta_arquivos, "configuracoes.txt")
acerto_txt                 = os.path.join(pasta_arquivos, "acertos.txt")

nivel = 1 #precisa ser definido antes para garantir que o codigo leia a lista de perguntas certa na hora de sua redefinição
nivel_atual_txt            = os.path.join(pasta_perguntas, "nivel" + str(nivel) + ".txt")

arquivo_img_normal_inicio   = os.path.join(pasta_imgs, "inicio.png")
arquivo_img_normal_config   = os.path.join(pasta_imgs, "configuraçao.png")
arquivo_img_zerado_inicio   = os.path.join(pasta_imgs, "inicio_1.png")
arquivo_img_zerado_config   = os.path.join(pasta_imgs, "configuraçao_1.png")
arquivo_img_verdade_botao   = os.path.join(pasta_imgs, "True_botao.png")
arquivo_img_falso_botao     = os.path.join(pasta_imgs, "False_botao.png")
arquivo_img_normal_credito1 = os.path.join(pasta_imgs, "credito1.png")
arquivo_img_normal_credito2 = os.path.join(pasta_imgs, "credito2.png")
arquivo_img_normal_credito3 = os.path.join(pasta_imgs, "credito3.png")
arquivo_img_normal_credito4 = os.path.join(pasta_imgs, "credito4.png")
arquivo_img_normal_sobre    = os.path.join(pasta_imgs, "sobre.png")
arquivo_img_normal_niveis   = os.path.join(pasta_imgs, "niveis.png")

arquivo_img_zerado_credito1 = os.path.join(pasta_imgs, "credito1_1.png")
arquivo_img_zerado_credito2 = os.path.join(pasta_imgs, "credito2_1.png")
arquivo_img_zerado_credito3 = os.path.join(pasta_imgs, "credito3_1.png")
arquivo_img_zerado_credito4 = os.path.join(pasta_imgs, "credito4_1.png")
arquivo_img_zerado_sobre    = os.path.join(pasta_imgs, "sobre_1.png")
arquivo_img_zerado_niveis   = os.path.join(pasta_imgs, "niveis_1.png")

arquivo_img_nivel1          = os.path.join(pasta_imgs, "nivel1.png")
arquivo_img_nivel2          = os.path.join(pasta_imgs, "nivel2.png")
arquivo_img_nivel3          = os.path.join(pasta_imgs, "nivel3.png")
arquivo_img_pergunta        = os.path.join(pasta_imgs, "pergunta.png")
arquivo_img_dica_botao      = os.path.join(pasta_imgs, "dica_botao.png")
arquivo_img_agradecimentos  = os.path.join(pasta_imgs, "agradecimentos.png")

arquivo_img_fundo_comum     = os.path.join(pasta_imgs, "fundo_0.png")
arquivo_img_fundo_zerado    = os.path.join(pasta_imgs, "fundo_1.png")

certo                       = os.path.join(pasta_icones, "certo.png")
parabens                    = os.path.join(pasta_icones, "parabens.png")
gpu                         = os.path.join(pasta_icones, "GPU.png")
hdd                         = os.path.join(pasta_icones, "HDD.png")
ram                         = os.path.join(pasta_icones, "RAM.png")
mouse                       = os.path.join(pasta_icones, "mouse.png")
gabinete                    = os.path.join(pasta_icones, "gabinete.png")
impressora                  = os.path.join(pasta_icones, "impressora.png")
notebook                    = os.path.join(pasta_icones, "notebook.png")
pendrive                    = os.path.join(pasta_icones, "pendrive.png")
placa_mae                   = os.path.join(pasta_icones, "placa_mae.png")
processador                 = os.path.join(pasta_icones, "processador.png")
monitores                   = os.path.join(pasta_icones, "monitores.png")
ventoinha                   = os.path.join(pasta_icones, "ventoinha.png")
teclado                     = os.path.join(pasta_icones, "teclado.png")

lista_dos_locais_dos_icones = gpu, hdd, ram, mouse, gabinete, impressora, notebook, pendrive, placa_mae, \
                    processador, monitores, ventoinha, teclado

# Carrega as configurações
res = (1280, 720)
volume = float()
dicas_ativas = bool()
salvar_acertos = bool()

# Resto do programa
pg.init()
screen = pg.display.set_mode(res)
pg.display.set_caption("Hard Time")

arquivo_a_ser_lido = config_txt
with open(arquivo_a_ser_lido, "r", encoding="utf-8") as arquivo_lido:
    linhas = arquivo_lido.readlines()

    for linha in linhas:
        if "volume:" in linha:
            volume = float(linha[7:len(linha)])
        if "dicas_ativas:" in linha:
            dicas_ativas = "True" in linha
        if "salvar_acertos" in linha:
            salvar_acertos = "True" in linha


transparente = pg.Surface((100, 100), pg.SRCALPHA)
transparente.fill((0, 0, 0, 0))  # preenche a superfície com cor totalmente transparente

#carregando sons
som_acerto         = pg.mixer.Sound(acerto_som_arquivo)
som_erro           = pg.mixer.Sound(erro_som_arquivo)
som_fim_do_tempo   = pg.mixer.Sound(tempo_esgotado_arquivo)
som_minuto_passado = pg.mixer.Sound(passou_um_minuto_arquivo)
tempo_alarme       = pg.mixer.Sound(tempo_som_arquivo)

musica = pg.mixer.Sound(lista_de_musicas[random.randint(0, 3)])
musica_channel = pg.mixer.find_channel()
sons_channel = pg.mixer.find_channel()
musica.set_volume(volume)
musica_channel.play(musica, loops=-1)

# Criando os botões (essas são posições para retangulos criados como identificadores do mouse, são originalmente invisiveis)
botao_abrir_config            = pg.Rect(  31,   42,   92,  112)
botao_salvar_acertos          = pg.Rect( 595,  380,   91,   41)
botao_aumentar_volume         = pg.Rect( 890,  572,   74,   89)
botao_diminuir_volume         = pg.Rect( 649,  572,   74,   89)
botao_de_ativar_dicas         = pg.Rect( 897,  349,   94,   43)
botao_sair_de_config          = pg.Rect(1080, 62, 108, 116)

botao_abrir_sobre             = pg.Rect(  45,  312,  425,  158)
botao_sair_de_sobre           = pg.Rect(1080, 62, 108, 116)

botao_abrir_creditos          = pg.Rect(  45,  498,  425,  158)
botao_proximo_creditos        = pg.Rect(1194,  323,   74,   74)
botao_voltar_creditos         = pg.Rect(   6, 323,  74,  74)
botao_sair_de_creditos        = pg.Rect(1090,  72,  90, 100)

botao_abrir_niveis            = pg.Rect( 440, 418, 398, 108)
botao_sair_de_niveis          = pg.Rect(1090,  72,  90, 100)

botao_abrir_nivel1_comum      = pg.Rect(147, 425, 118, 112)
botao_abrir_nivel2_comum      = pg.Rect(599, 337, 118, 112)
botao_abrir_nivel3_comum      = pg.Rect(996, 393, 118, 112)

botao_abrir_nivel1_tema       = pg.Rect( 97, 569, 215, 110)
botao_abrir_nivel2_tema       = pg.Rect(553, 481, 215, 110)
botao_abrir_nivel3_tema       = pg.Rect(941, 543, 215, 110)

botao_sair_de_nivel1          = pg.Rect(1080, 62, 108, 116)
botao_sair_de_nivel2          = pg.Rect(1080, 62, 108, 116)
botao_sair_de_nivel3          = pg.Rect(1080, 62, 108, 116)

botao_nivel1_comecar          = pg.Rect(449, 444, 375,  90)
botao_nivel2_comecar          = pg.Rect(449, 444, 375,  90)
botao_nivel3_comecar          = pg.Rect(449, 444, 375,  90)

botao_sair_de_pergunta        = pg.Rect(1160,  42,   98,  96)
botao_de_dica                 = pg.Rect(  16, 596,  102, 102)

botao_alternativa_a           = pg.Rect(105, 325,  53, 53)
botao_alternativa_b           = pg.Rect(105, 400,  53, 53)
botao_alternativa_c           = pg.Rect(105, 475,  53, 53)
botao_alternativa_d           = pg.Rect(105, 550,  53, 53)

botao_agradecimentos_em_inicio   = pg.Rect( 943,   0, 138, 168)
botao_agradecimentos_em_config   = pg.Rect( 823,  29, 158, 193)
botao_agradecimentos_em_creditos = pg.Rect( 555,  29, 159, 194)
botao_agradecimentos_em_sobre    = pg.Rect( 414,  29, 158, 193)
botao_agradecimentos_em_niveis   = pg.Rect( 403,  29, 158, 193)
botao_sair_de_agradecimentos     = pg.Rect(1130,  35, 104, 163)

botao_algol                      = pg.Rect( 87, 457, 89, 89) 
botao_numero_da_pergunta         = pg.Rect(176, 112, 79, 79) 

botao_de_fechar_o_jogo           = pg.Rect( 45, 607, 100, 48)

# Cria os cursores
cursor_seta     = pg.Cursor(pg.SYSTEM_CURSOR_ARROW)
cursor_mao      = pg.Cursor(pg.SYSTEM_CURSOR_HAND)

#imgs que não são alteradas
img_gpu             = pg.image.load(gpu)
img_hdd             = pg.image.load(hdd)
img_ram             = pg.image.load(ram)
img_mouse           = pg.image.load(mouse)
img_monitores       = pg.image.load(monitores)
img_gabinete        = pg.image.load(gabinete)
img_ventoinha       = pg.image.load(ventoinha)
img_impressora      = pg.image.load(impressora)
img_pendrive        = pg.image.load(pendrive)
img_teclado         = pg.image.load(teclado)
img_processador     = pg.image.load(processador)
img_notebook        = pg.image.load(notebook)
img_placa_mae       = pg.image.load(placa_mae)
tupla_de_icones_img = img_gpu, img_hdd, img_ram, img_mouse, img_monitores, img_gabinete, img_ventoinha, \
    img_placa_mae, img_notebook, img_impressora, img_teclado, img_pendrive

img_certo           = pg.image.load(certo)
img_nivel1          = pg.image.load(arquivo_img_nivel1)
img_nivel2          = pg.image.load(arquivo_img_nivel2)
img_nivel3          = pg.image.load(arquivo_img_nivel3)
img_pergunta        = pg.image.load(arquivo_img_pergunta)
img_dica_botao      = pg.image.load(arquivo_img_dica_botao)
img_agradecimentos  = pg.image.load(arquivo_img_agradecimentos)

# Definindo a tela ativa
tela_ativa = "inicio"

#Variáveis do sistema
acertos = 0
erros = 0
numero_de_perguntas = 0
quantidade_de_perguntas = 0
quantidade_de_perguntas_nivel1 = 0
quantidade_de_perguntas_nivel2 = 0
quantidade_de_perguntas_nivel3 = 0
x_movimentavel       = 0
y_movimentavel       = 0
x_de_movimencacao    = 10
y_de_movimencacao    = 0
x_inicial, y_inicial = 0, 0
x_final, y_final     = 0, 0
rotate, rodador = 0.0, 0
fade_icone = 0
index = 0
mover_icone = True

for nivel_atual in range(1,3+1): #Número do primeiro nível e número do último +1
    arquivo_do_nivel_atual = os.path.join(pasta_perguntas, "nivel"+str(nivel_atual)+".txt")

    with open(arquivo_do_nivel_atual, 'r', encoding='utf-8') as contador_de_linhas:
        numero_de_linhas = len(contador_de_linhas.readlines())
        quantidade_de_perguntas = (numero_de_linhas)//12+1
        if nivel_atual == 1:
            quantidade_de_perguntas_nivel1 = quantidade_de_perguntas
        if nivel_atual == 2:
            quantidade_de_perguntas_nivel2 = quantidade_de_perguntas
        if nivel_atual == 3:
            quantidade_de_perguntas_nivel3 = quantidade_de_perguntas

resposta = 0

tick = 0
index_de_cauculo = 0
tempo_max = ""
segundos_max = int()
minutos_max = int()
segundos = segundos_max
minutos = minutos_max

frame_atual = -1
nivel1_acertos = 0
nivel2_acertos = 0
nivel3_acertos = 0
alternativa1 = ""
alternativa2 = ""
alternativa3 = ""
alternativa4 = ""
str_num_pergunta = ""
nivel1_acertos_antes = 0
nivel2_acertos_antes = 0
nivel3_acertos_antes = 0
dica = ""
mostra_dica = ""

quero_mais_que_sete = False
primeiro_falta_quinze = False

icone_atual = pg.Surface((100, 100), pg.SRCALPHA)

defini_o_incone_aleatoriamente()

if salvar_acertos:
    arquivo = acerto_txt

    with open(arquivo, "r", encoding="utf-8") as arquivo_lido:
        linhas = arquivo_lido.readlines()
        
        for linha in linhas:
            
            if not linha:
                break
            if "nivel 1:" in linha:
                nivel1_acertos_antes = int(linha[8:len(linha)])
            if "nivel 2:" in linha:
                nivel2_acertos_antes = int(linha[8:len(linha)])
            if "nivel 3:" in linha:
                nivel3_acertos_antes = int(linha[8:len(linha)])

nivel1_acertos = nivel1_acertos_antes
nivel2_acertos = nivel2_acertos_antes
nivel3_acertos = nivel3_acertos_antes

sistema_de_fps = pg.time.Clock()

while True:
    sistema_de_fps.tick(60)

    mouse = pg.mouse.get_pos()
    carrega_configuracoes()
    
    o_melhor_nerd = True if nivel1_acertos == quantidade_de_perguntas_nivel1 \
        and nivel2_acertos == quantidade_de_perguntas_nivel2 \
            and nivel3_acertos == quantidade_de_perguntas_nivel3 else False

    if not o_melhor_nerd: 
        # Carregando as imagens se tiver zerado
        # Elas devem estar dentro da pasta imagens
        img_inicio      = pg.image.load(arquivo_img_normal_inicio)
        img_config      = pg.image.load(arquivo_img_normal_config)
        img_credito1      = pg.image.load(arquivo_img_normal_credito1)
        img_credito2      = pg.image.load(arquivo_img_normal_credito2)
        img_credito3      = pg.image.load(arquivo_img_normal_credito3)
        img_credito4      = pg.image.load(arquivo_img_normal_credito4)
        img_sobre       = pg.image.load(arquivo_img_normal_sobre)
        img_niveis      = pg.image.load(arquivo_img_normal_niveis)

        img_fundo  = pg.image.load(arquivo_img_fundo_comum)
    else:
        # Carregando as imagens se não tiver zerado
        # Elas devem estar dentro da pasta imagens
        img_inicio      = pg.image.load(arquivo_img_zerado_inicio)
        img_config      = pg.image.load(arquivo_img_zerado_config)
        img_credito1    = pg.image.load(arquivo_img_zerado_credito1)
        img_credito2    = pg.image.load(arquivo_img_zerado_credito2)
        img_credito3    = pg.image.load(arquivo_img_zerado_credito3)
        img_credito4    = pg.image.load(arquivo_img_zerado_credito4)
        img_sobre       = pg.image.load(arquivo_img_zerado_sobre)
        img_niveis      = pg.image.load(arquivo_img_zerado_niveis)

        img_fundo  = pg.image.load(arquivo_img_fundo_zerado)

    screen.blit(img_fundo, (0,0))


    if tela_ativa == "inicio":
        if mover_icone:
            movi_o_icone()
        screen.blit(img_inicio, (0, -41))

        if botao_de_fechar_o_jogo.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_de_fechar_o_jogo, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_abrir_config.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_abrir_config, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_abrir_niveis.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_abrir_niveis, width=4, border_radius=60)
            pg.mouse.set_cursor(cursor_mao)
        elif o_melhor_nerd and botao_agradecimentos_em_inicio.collidepoint(mouse):
            pg.mouse.set_cursor(cursor_mao)
        else:
            pg.mouse.set_cursor(cursor_seta)

    elif tela_ativa == "config":
        img_salvar_acertos  = pg.image.load(arquivo_img_verdade_botao if salvar_acertos else arquivo_img_falso_botao)
        img_dicas_ativas    = pg.image.load(arquivo_img_verdade_botao if dicas_ativas   else arquivo_img_falso_botao)

        volume_texto = pg.font.Font(fonte_bauhs, 54).render(str(int(volume*100)), True, (255, 255, 255))
        screen.blit(img_config, (0, 0))
        screen.blit(volume_texto, (793-10*len(str(int(volume*100))), 580))
        screen.blit(img_salvar_acertos, (595, 380))
        screen.blit(img_dicas_ativas, (899, 350))

        if botao_sair_de_config.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_sair_de_config, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_abrir_sobre.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_abrir_sobre, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_abrir_creditos.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_abrir_creditos, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_diminuir_volume.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_diminuir_volume, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_aumentar_volume.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_aumentar_volume, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_de_ativar_dicas.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_de_ativar_dicas, width=4, border_radius=29)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_salvar_acertos.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_salvar_acertos, width=4, border_radius=29)
            pg.mouse.set_cursor(cursor_mao)
        else:
            pg.mouse.set_cursor(cursor_seta)


    elif tela_ativa == "sobre":
        screen.blit(img_sobre, (0, 0))

        if botao_sair_de_sobre.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_sair_de_sobre, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif o_melhor_nerd and botao_agradecimentos_em_sobre.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_agradecimentos_em_sobre, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        else:
            pg.mouse.set_cursor(cursor_seta)

    elif tela_ativa == "credito1":
        screen.blit(img_credito1, (0, 0))

        if botao_sair_de_creditos.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_sair_de_creditos, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_proximo_creditos.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_proximo_creditos, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        
        else:
            pg.mouse.set_cursor(cursor_seta)


    elif tela_ativa == "credito2":
        screen.blit(img_credito2, (-120, -208))

        if botao_sair_de_creditos.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_sair_de_creditos, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_proximo_creditos.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_proximo_creditos, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_voltar_creditos.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_voltar_creditos, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        
        else:
            pg.mouse.set_cursor(cursor_seta)

    elif tela_ativa == "credito2":
        screen.blit(img_credito2, (-120, -208))

        if botao_sair_de_creditos.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_sair_de_creditos, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_proximo_creditos.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_proximo_creditos, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_voltar_creditos.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_voltar_creditos, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        
        else:
            pg.mouse.set_cursor(cursor_seta)

    elif tela_ativa == "credito3":
        screen.blit(img_credito3, (-161, -159))

        if botao_sair_de_creditos.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_sair_de_creditos, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_proximo_creditos.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_proximo_creditos, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_voltar_creditos.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_voltar_creditos, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        
        else:
            pg.mouse.set_cursor(cursor_seta)

    elif tela_ativa == "credito4":
        screen.blit(img_credito4, (0, 0))

        if botao_sair_de_creditos.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_sair_de_creditos, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_voltar_creditos.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_voltar_creditos, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        
        else:
            pg.mouse.set_cursor(cursor_seta)

    elif tela_ativa == "niveis":
        musica_channel.unpause()
        screen.blit(img_niveis, (0, 0))
        if nivel1_acertos == 11:
            screen.blit(pg.image.load(parabens), (11, 311))
        if nivel2_acertos == 15:
            screen.blit(pg.image.load(parabens), (458, 211))
        if nivel3_acertos == 20:
            screen.blit(pg.image.load(parabens), (854, 274))
        if salvar_acertos:
            carrega_acertos()
        pontuacao()

        if botao_sair_de_niveis.collidepoint(mouse):
            pg.draw.rect(screen, (0, 0, 0), botao_sair_de_niveis, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)

        elif botao_abrir_nivel1_comum.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_abrir_nivel1_comum, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_abrir_nivel1_tema.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_abrir_nivel1_tema, width=4, border_radius=80)
            pg.mouse.set_cursor(cursor_mao)
            
        elif botao_abrir_nivel2_comum.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_abrir_nivel2_comum, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_abrir_nivel2_tema.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_abrir_nivel2_tema, width=4, border_radius=80)
            pg.mouse.set_cursor(cursor_mao)

        elif botao_abrir_nivel3_comum.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_abrir_nivel3_comum, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_abrir_nivel3_tema.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_abrir_nivel3_tema, width=4, border_radius=80)
            pg.mouse.set_cursor(cursor_mao)

        elif o_melhor_nerd and botao_agradecimentos_em_niveis.collidepoint(mouse):
            pg.mouse.set_cursor(cursor_mao)

        else:
            pg.mouse.set_cursor(cursor_seta)

    elif tela_ativa == "nivel1":
        screen.blit(img_nivel1, (0, 0))
        nivel = 1
        nivel_atual_txt = os.path.join(pasta_perguntas, "nivel" + str(nivel) + ".txt")
        
        if botao_nivel1_comecar.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_nivel1_comecar, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_sair_de_nivel1 .collidepoint(mouse):
            pg.draw.rect(screen, (0, 0, 0), botao_sair_de_nivel1, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)

        else:
            pg.mouse.set_cursor(cursor_seta)

    elif tela_ativa == "nivel2":
        screen.blit(img_nivel2, (0, 0))
        nivel = 2
        nivel_atual_txt = os.path.join(pasta_perguntas, "nivel" + str(nivel) + ".txt")

        if botao_nivel2_comecar.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_nivel2_comecar, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_sair_de_nivel2 .collidepoint(mouse):
            pg.draw.rect(screen, (0, 0, 0), botao_sair_de_nivel2, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)

        else:
            pg.mouse.set_cursor(cursor_seta)

    elif tela_ativa == "nivel3":
        screen.blit(img_nivel3, (0, 0))
        nivel = 3
        nivel_atual_txt = os.path.join(pasta_perguntas, "nivel" + str(nivel) + ".txt")

        if botao_nivel3_comecar.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_nivel3_comecar, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_sair_de_nivel3 .collidepoint(mouse):
            pg.draw.rect(screen, (0, 0, 0), botao_sair_de_nivel3, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)

        else:
            pg.mouse.set_cursor(cursor_seta)

    elif tela_ativa == "pergunta":
        screen.blit(img_pergunta, (0, 0))
        screen.blit(img_dica_botao, (16, 596))

        if botao_sair_de_pergunta.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_sair_de_pergunta, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)

        elif dicas_ativas and botao_de_dica.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_de_dica, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)

        elif botao_alternativa_a.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_alternativa_a, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_alternativa_b.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_alternativa_b, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_alternativa_c.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_alternativa_c, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)
        elif botao_alternativa_d.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_alternativa_d, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)

        else:
            pg.mouse.set_cursor(cursor_seta)
                
        if musica_channel.get_busy():
            musica_channel.pause()
        carregar_pergunta()

        if nivel == 1 and numero_de_perguntas+1 == 11 and mostra_dica != "":
            if botao_algol.collidepoint(mouse):
                mostra_dica = "GOOOOOOOOLL!!!"
            else:
                mostra_dica = "oLhA o GOL! oLhA o GOL!"

        if nivel == 2 and numero_de_perguntas+1 == 15 and mostra_dica != "":
            alternativa1, alternativa3, alternativa4 = "", "", ""

        if nivel == 3 and numero_de_perguntas+1 == 1 and mostra_dica != "":
            str_num_pergunta = "4" if botao_numero_da_pergunta.collidepoint(mouse) else str(numero_de_perguntas+1)

    elif tela_ativa == "agradecimento":
        if botao_sair_de_agradecimentos.collidepoint(mouse):
            pg.draw.rect(screen, (255, 255, 255), botao_sair_de_agradecimentos, width=4, border_radius=20)
            pg.mouse.set_cursor(cursor_mao)

        else:
            pg.mouse.set_cursor(cursor_seta)

        screen.blit(img_agradecimentos, (0,0))


    #Eventos-----------------------------------------------------------


    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            salva_configuracoes()
            pg.quit()
            exit()

        elif ev.type == pg.KEYDOWN:
            if ev.key == pg.K_F11:
                if pg.display.is_fullscreen():
                    res = (1280, 720)
                else:
                    res = pg.display.toggle_fullscreen()

        elif ev.type == pg.MOUSEBUTTONDOWN:

            if ev.type == pg.MOUSEWHEEL:
                continue

            if tela_ativa == "inicio":
                if botao_abrir_config.collidepoint(mouse):
                     tela_ativa = "config"
                     mover_icone = False
                     
                if botao_abrir_niveis.collidepoint(mouse):
                     tela_ativa = "niveis"
                     mover_icone = False
                     
                if o_melhor_nerd:
                    if botao_agradecimentos_em_inicio.collidepoint(mouse):
                     tela_ativa = "agradecimento"
                     trocar_para_agradecimentos = True
                     mover_icone = False
                     
                if botao_de_fechar_o_jogo.collidepoint(mouse):
                    salva_configuracoes()
                    pg.quit()
                    exit()

            elif tela_ativa == "config":
                if botao_sair_de_config.collidepoint(mouse):
                     tela_ativa = "inicio"
                     defini_o_incone_aleatoriamente()
                     mover_icone = True
                     
                if botao_salvar_acertos.collidepoint(mouse):
                    salvar_acertos = True if not salvar_acertos else False
                if botao_de_ativar_dicas.collidepoint(mouse):
                    dicas_ativas = True if not dicas_ativas else False
                if botao_diminuir_volume.collidepoint(mouse):
                    volume -= 0.1
                    verifica_o_volume()
                    musica.set_volume(volume)
                if botao_aumentar_volume.collidepoint(mouse):
                    if volume == 0.7:
                        quero_mais_que_sete = True
                    else:
                        volume += 0.1
                    verifica_o_volume()
                    quero_mais_que_sete = False
                    if "0.79" in str(volume):
                        volume = 0.8
                    musica.set_volume(volume)
                if botao_abrir_sobre.collidepoint(mouse):
                     tela_ativa = "sobre"
                     
                if botao_abrir_creditos.collidepoint(mouse):
                     tela_ativa = "credito1"
                     
                if o_melhor_nerd and botao_agradecimentos_em_config.collidepoint(mouse):
                     tela_ativa = "agradecimento"                     

            elif tela_ativa == "sobre":
                if botao_sair_de_sobre.collidepoint(mouse):
                     tela_ativa = "config"
                     
                if o_melhor_nerd and botao_agradecimentos_em_sobre.collidepoint(mouse):
                     tela_ativa = "agradecimento"                     

            elif tela_ativa == "credito1":
                if botao_sair_de_creditos.collidepoint(mouse):
                     tela_ativa = "config"
                     
                if botao_proximo_creditos.collidepoint(mouse):
                     tela_ativa = "credito2"
                     
                if o_melhor_nerd and botao_agradecimentos_em_creditos.collidepoint(mouse):
                     tela_ativa = "agradecimento"
                     trocar_para_agradecimento = True
                     
                    
            elif tela_ativa == "credito2":
                if botao_sair_de_creditos.collidepoint(mouse):
                     tela_ativa = "config"
                     
                if botao_voltar_creditos.collidepoint(mouse):
                     tela_ativa = "credito1"
                     
                if botao_proximo_creditos.collidepoint(mouse):
                     tela_ativa = "credito3"
                     
                if o_melhor_nerd and botao_agradecimentos_em_creditos.collidepoint(mouse):
                     tela_ativa = "agradecimento"
                     

            elif tela_ativa == "credito3":
                if botao_sair_de_creditos.collidepoint(mouse):
                     tela_ativa = "config"
                     
                if botao_voltar_creditos.collidepoint(mouse):
                     tela_ativa = "credito2"
                     
                if botao_proximo_creditos.collidepoint(mouse):
                     tela_ativa = "credito4"
                     
                if o_melhor_nerd and botao_agradecimentos_em_creditos.collidepoint(mouse):
                     tela_ativa = "agradecimento"

            elif tela_ativa == "credito4":
                if botao_sair_de_creditos.collidepoint(mouse):
                     tela_ativa = "config"
                     
                if botao_voltar_creditos.collidepoint(mouse):
                     tela_ativa = "credito3"
                     
                if o_melhor_nerd and botao_agradecimentos_em_creditos.collidepoint(mouse):
                     tela_ativa = "agradecimento"
                     

            elif tela_ativa == "niveis":
                if botao_sair_de_niveis.collidepoint(mouse):
                     tela_ativa = "inicio"
                     defini_o_incone_aleatoriamente()
                     mover_icone = True

                if botao_abrir_nivel1_comum.collidepoint(mouse) or \
                    botao_abrir_nivel1_tema.collidepoint(mouse):
                     tela_ativa = "nivel1"
                     
                if botao_abrir_nivel2_comum.collidepoint(mouse) or \
                    botao_abrir_nivel2_tema.collidepoint(mouse):
                     tela_ativa = "nivel2"
                     
                if botao_abrir_nivel3_comum.collidepoint(mouse) or \
                    botao_abrir_nivel3_tema.collidepoint(mouse):
                     tela_ativa = "nivel3"
                     
                if o_melhor_nerd and botao_agradecimentos_em_niveis.collidepoint(mouse):
                     tela_ativa = "agradecimento"                     


            elif tela_ativa == "nivel1":
                if botao_sair_de_nivel1.collidepoint(mouse):
                     tela_ativa = "niveis"

                     
                if botao_nivel1_comecar.collidepoint(mouse):
                    if salvar_acertos and nivel1_acertos >= nivel1_acertos_antes:
                        salva_acertos()

                    tela_ativa = "pergunta"
                    timer_finalizado = True
                    
                    nivel1_acertos = 0

            elif tela_ativa == "nivel2":
                if botao_sair_de_nivel2.collidepoint(mouse):
                     tela_ativa = "niveis"
                     
                if botao_nivel2_comecar.collidepoint(mouse):
                    if salvar_acertos and nivel2_acertos >= nivel2_acertos_antes:
                        salva_acertos()

                    tela_ativa = "pergunta"
                    trocar_para_nivel2 = True
                    timer_finalizado = True
                    primeiro_falta_quinze = True
                    nivel2_acertos = 0

            elif tela_ativa == "nivel3":
                if botao_sair_de_nivel3.collidepoint(mouse):
                     tela_ativa = "niveis"

                if botao_nivel3_comecar.collidepoint(mouse):
                    tela_ativa = "pergunta"
                    timer_finalizado = True
                    primeiro_falta_quinze = True
                    nivel3_acertos = 0


            elif tela_ativa == "agradecimento":
                if o_melhor_nerd and botao_sair_de_agradecimentos.collidepoint(mouse):
                     tela_ativa = "inicio"
                     defini_o_incone_aleatoriamente()
                     mover_icone = True

            elif tela_ativa == "pergunta":
                if botao_de_dica.collidepoint(mouse):
                    mostra_dica = dica if dicas_ativas else ""
                if botao_sair_de_pergunta.collidepoint(mouse):
                    mostra_dica = ""
                    tela_ativa = "niveis"
                    
                if botao_alternativa_a.collidepoint(mouse):
                    mostra_dica = ''
                    if resposta == 1:
                        screen.blit(img_certo, (105, 325))
                        acertou()
                    else:
                        errou()
                if botao_alternativa_b.collidepoint(mouse):
                    mostra_dica = ''
                    if resposta == 2:
                        screen.blit(img_certo, (105, 400))
                        acertou()
                    else:
                        errou()
                if botao_alternativa_c.collidepoint(mouse):
                    mostra_dica = ''
                    if resposta == 3:
                        screen.blit(img_certo, (105, 475))
                        acertou()
                    else:
                        errou()
                if botao_alternativa_d.collidepoint(mouse):
                    mostra_dica = ''
                    if resposta == 4:
                        screen.blit(img_certo, (105, 550))
                        acertou()
                    else:
                        errou()

                if numero_de_perguntas >= quantidade_de_perguntas-1:
                    numero_de_perguntas = 0
                    if salvar_acertos and nivel1_acertos >= nivel1_acertos_antes and \
                        nivel2_acertos >= nivel2_acertos_antes and \
                        nivel3_acertos >= nivel3_acertos_antes:
                        salva_acertos()

                    tela_ativa = "niveis" if not o_melhor_nerd else "agradecimento"
                    

    pg.display.flip()