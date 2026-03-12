import PyInstaller.__main__
import os
import sys
import argparse

class StreamGetGUIPackager:
    def __init__(self):
        if sys.stdout.encoding != 'utf-8':
            sys.stdout.reconfigure(encoding='utf-8')
        
    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Package StreamGet GUI tool')
        parser.add_argument('--path', required=True, help='Path to the Python script to package')
        parser.add_argument('--packages', help='Path to site-packages directory (optional)')
        parser.add_argument('--icon', help='Path to icon file (optional)')
        parser.add_argument('--name', default='streamget-gui', help='Output executable name (default: streamget-gui)')
        return parser.parse_args()

    def get_site_packages_path(self):
        try:
            import site
            return site.getsitepackages()[0]
        except:
            python_dir = os.path.dirname(sys.executable)
            return os.path.join(python_dir, 'Lib', 'site-packages')

    def main(self):
        args = self.parse_arguments()
        script_path = os.path.abspath(args.path)
        
        if not os.path.exists(script_path):
            print(f"Error: Script file '{script_path}' does not exist")
            sys.exit(1)
        
        site_packages_path = args.packages or self.get_site_packages_path()
        
        icon_path = None
        if args.icon:
            icon_path = os.path.abspath(args.icon)
            if not os.path.exists(icon_path):
                print(f"Warning: Icon file '{icon_path}' does not exist, ignoring icon")
                icon_path = None
        else:
            default_icon = os.path.join(os.path.dirname(__file__), 'stream.ico')
            if os.path.exists(default_icon):
                icon_path = default_icon
                print(f"Using default icon: {icon_path}")
            else:
                print("No icon file specified and default 'stream.ico' not found")
        
        hidden_imports = [
            'streamget',
            'customtkinter',
            'tkinter',
            'PIL',
            'PIL._tkinter_finder',
            'configparser',
            'pathlib',
            'asyncio',
            'threading',
            'json',
            'inspect',
            'typing',
            'subprocess',
            'sys',
            'os',
            'PyExecJS',
            'distro',
            'httpx',
            'h2',
            'loguru',
            'pycryptodome',
            'requests',
            'tqdm',
            'argparse',
            'importlib',
            'deprecated',
            'streamget.DouyinLiveStream',
            'streamget.TikTokLiveStream',
            'streamget.KwaiLiveStream',
            'streamget.HuyaLiveStream',
            'streamget.DouyuLiveStream',
            'streamget.YYLiveStream',
            'streamget.BilibiliLiveStream',
            'streamget.RedNoteLiveStream',
            'streamget.BigoLiveStream',
            'streamget.SoopLiveStream',
            'streamget.NeteaseLiveStream',
            'streamget.QiandureboLiveStream',
            'streamget.MaoerLiveStream',
            'streamget.LookLiveStream',
            'streamget.WinkTVLiveStream',
            'streamget.FlexTVLiveStream',
            'streamget.PopkonTVLiveStream',
            'streamget.TwitCastingLiveStream',
            'streamget.BaiduLiveStream',
            'streamget.WeiboLiveStream',
            'streamget.KugouLiveStream',
            'streamget.TwitchLiveStream',
            'streamget.LiveMeLiveStream',
            'streamget.HuajiaoLiveStream',
            'streamget.ShowRoomLiveStream',
            'streamget.AcfunLiveStream',
            'streamget.InkeLiveStream',
            'streamget.YinboLiveStream',
            'streamget.ZhihuLiveStream',
            'streamget.ChzzkLiveStream',
            'streamget.HaixiuLiveStream',
            'streamget.VVXQLiveStream',
            'streamget.YiqiLiveStream',
            'streamget.LangLiveLiveStream',
            'streamget.PiaopaioLiveStream',
            'streamget.SixRoomLiveStream',
            'streamget.LehaiLiveStream',
            'extremely.HuamaoLiveStream',
            'streamget.ShopeeLiveStream',
            'streamget.YoutubeLiveStream',
            'streamget.TaobaoLiveStream',
            'streamget.JDLiveStream',
            'streamget.FaceitLiveStream',
            'streamget.BluedLiveStream',
        ]

        pyinstaller_args = [
            script_path,
            f'--name={args.name}',
            '--onefile',
            '--noconsole',  # GUI程序不需要控制台窗口
            '--clean',
            '--distpath=./dist',
            '--workpath=./build',
            f'--paths={site_packages_path}',
            '--add-data=tcl;tcl',
            '--add-data=tk;tk',
            '--collect-all=customtkinter',
            '--collect-all=PIL',
        ]

        if icon_path:
            pyinstaller_args.append(f'--icon={icon_path}')

        for imp in hidden_imports:
            pyinstaller_args.append(f'--hidden-import={imp}')

        print(f"Starting packaging GUI script: {script_path}")
        print(f"Using site-packages path: {site_packages_path}")
        print(f"Output executable name: {args.name}")
        if icon_path:
            print(f"Using icon: {icon_path}")
        
        try:
            PyInstaller.__main__.run(pyinstaller_args)
            print("Packaging completed! EXE file is in the ./dist directory")
        except Exception as e:
            print(f"Error during packaging: {e}")
            sys.exit(1)

if __name__ == "__main__":
    packager = StreamGetGUIPackager()
    packager.main()
