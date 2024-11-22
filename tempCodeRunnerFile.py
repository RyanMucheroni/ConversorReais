import requests
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.window import Window

class ManipulaJanela:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

    def ajustar_tamanho_janela(self):
        Window.size = (self.largura, self.altura)

class MeuApp(MDApp):
    def build(self):
        manipulador = ManipulaJanela(400, 600)
        manipulador.ajustar_tamanho_janela()

        # Criando o layout principal
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        # Campo de entrada para a quantidade em reais
        self.entrada_dados = MDTextField(
            hint_text="Digite o valor em Reais",
            helper_text="Exemplo: 100.00",
            helper_text_mode="on_focus",
            id="entrada_dados"
        )
        layout.add_widget(self.entrada_dados)

        # Menu suspenso para selecionar a moeda de conversão
        self.moeda_spinner = MDTextField(
            hint_text="Escolha a moeda (USD ou EUR)",
            id="moeda_spinner"
        )
        layout.add_widget(self.moeda_spinner)

        # Botão para converter a quantidade para a moeda selecionada
        botao_converter = MDRaisedButton(text="Converter", on_release=self.converter_moeda)
        layout.add_widget(botao_converter)

        # Área de saída de dados
        self.saida_dados = MDLabel(
            text="Resultado: ",
            halign="left",
            id="saida_dados"
        )
        layout.add_widget(self.saida_dados)

        return layout

    def converter_moeda(self, instance):
        entrada_dados = self.entrada_dados.text
        saida_dados = self.saida_dados
        moeda = self.moeda_spinner.text.upper()

        # Verifica se a moeda selecionada é válida
        if moeda not in ["USD", "EUR"]:
            saida_dados.text = "Selecione uma moeda válida (USD ou EUR)."
            return

        try: #converte o valor inserido em número
            valor_reais = float(entrada_dados)  # Converte o valor inserido para número
            url = 'https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL'  # URL da API de câmbio
            response = requests.get(url)  # Faz a requisição para a API
            data = response.json()  # Converte a resposta da API para JSON

            # Verifica a moeda e faz a conversão
            if moeda == "USD" and 'USDBRL' in data:
                taxa_cambio = float(data['USDBRL']['bid'])  # Obtém a taxa de venda USD/BRL
                valor_convertido = valor_reais / taxa_cambio  # Realiza a conversão
                saida_dados.text = f"R$ {valor_reais:.2f} é igual a ${valor_convertido:.2f} dólares."
            elif moeda == "EUR" and 'EURBRL' in data:
                taxa_cambio = float(data['EURBRL']['bid'])  # Obtém a taxa de venda EUR/BRL
                valor_convertido = valor_reais / taxa_cambio  # Realiza a conversão
                saida_dados.text = f"R$ {valor_reais:.2f} é igual a €{valor_convertido:.2f} euros."
            else:
                saida_dados.text = 'Erro ao obter a conversão.'  # Caso não consiga fazer a conversão
        except ValueError:
            saida_dados.text = 'Por favor, insira um valor numérico válido.'  # Caso o valor inserido não seja numérico


MeuApp().run()