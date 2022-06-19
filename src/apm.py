import wx.lib.mixins.inspection

from myWX.AssetPackageManagerFrame import AssetPackageManagerFrame


class AssetPackageManagerApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    """APM application class"""

    def OnInit(self):
        self.Init()
        frame = AssetPackageManagerFrame(None, -1, "Asset Package Manager")
        frame.Show()
        return True


if __name__ == '__main__':
    app = AssetPackageManagerApp()
    app.MainLoop()
