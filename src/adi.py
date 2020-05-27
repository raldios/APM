import wx.lib.mixins.inspection

from myWX.MainFrame import MainFrame


class AssetPackageManagerApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    """APM application class"""

    def OnInit(self):
        self.Init()
        frame = MainFrame(None, -1, "Asset Package Manager")
        frame.Show()
        return True


if __name__ == '__main__':
    app = AssetPackageManagerApp()
    app.MainLoop()
