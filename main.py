from modules import CoolText, PostChangeConfigOptions

config = PostChangeConfigOptions(LogoID="732440996", Text="Hello World")
print(CoolText(config).create())
