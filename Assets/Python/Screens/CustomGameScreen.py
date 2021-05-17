# ccgs
from CvPythonExtensions import *
import GenericDecoratedScreen
import CvUtil
import ScreenInput
import CvScreenEnums


gc = CyGlobalContext()
#ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()


class CustomGameScreen(GenericDecoratedScreen.GenericDecoratedScreen):
	"Exotic Foreign Advisor Screen"

	def __init__(self):
		GenericDecoratedScreen.GenericDecoratedScreen.__init__(self)
		self.iScreenID = CvScreenEnums.CUSTOM_GAME_SCREEN


	def getScreen(self): # override
		return CyGInterfaceScreen("CustomGameScreen", self.iScreenID)


	def interfaceScreen(self):
		screen = self.getScreen()
		self.initDimensions()
		self.addBackgroundHeaderFooter(localText.getText("TXT_KEY_CUSTOM_GAME_TITLE", ()))

		panelMargin = 10
		panelWidth = self.wScreen - 2 * panelMargin
		panelHeight = self.hScreen - 2 * panelMargin - self.hHeader - self.hFooter
		screen.addPanel("TestPanel", "", "", True, True,
				panelMargin, panelMargin + self.hFooter, panelWidth, panelHeight,
				PanelStyles.PANEL_STYLE_MAIN)

		self.GAMESPEED_DROPDOWN_ID = "GameSpeedDropDown"
		screen.addDropDownBoxGFC(self.GAMESPEED_DROPDOWN_ID, panelWidth // 2, panelHeight // 2, 200, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i in reversed(range(gc.getNumGameSpeedInfos())):
			# Not going to add a "Random" choice for the moment
			screen.addPullDownString(self.GAMESPEED_DROPDOWN_ID, gc.getGameSpeedInfo(i).getDescription(), i, i, i == gc.getInitCore().getGameSpeed())

		screen.setText(self.EXIT_ID, "Background",
				u"<font=4>" + localText.getText("TXT_KEY_MAIN_MENU_LAUNCH", ()).upper() + "</font>",
				CvUtil.FONT_RIGHT_JUSTIFY, self.xExitButton, self.yExitButton, 0,
				FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN,
				self.iScreenID, 0) # 0 TAB presses, then Enter.
		screen.setActivation(self.EXIT_ID, ActivationTypes.ACTIVATE_NORMAL)
		GOBACK_ID = "GoBackButton"
		xGoBackButton = 130
		screen.setText(GOBACK_ID, "Background",
				u"<font=4>" + localText.getText("TXT_KEY_MAIN_MENU_GO_BACK", ()).upper() + "</font>",
				CvUtil.FONT_RIGHT_JUSTIFY, xGoBackButton, self.yExitButton, 0,
				FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN,
				self.iScreenID, 1) # One TAB press, then Enter.
		screen.setActivation(GOBACK_ID, ActivationTypes.ACTIVATE_NORMAL)
		footerButtonDist = 300 # Distance in between footer buttons that are grouped together
		CLOSE_ID = "CloseButton"
		screen.setText(CLOSE_ID, "Background",
				u"<font=4>" + localText.getText("TXT_KEY_CUCUGS_CLOSE", ()).upper() + "</font>",
				CvUtil.FONT_RIGHT_JUSTIFY, xGoBackButton + footerButtonDist, self.yExitButton, 0,
				FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN,
				-1, -1) # Regular close-screen widget; no simulated key presses.
		screen.setActivation(CLOSE_ID, ActivationTypes.ACTIVATE_NORMAL)

		# This doesn't seem to affect anything
		#screen.setCloseOnEscape(False)
		# Without this, calls to interfaceScreen don't bring the screen back after ESC.
		screen.setPersistent(True)
		# This leads to a crash. I'm trying to prevent players from TAB-selecting widgets
		# on the original screen in the background ... open issue.
		#screen.setMainInterface(True)
		# Should we use bPassInput=True? The Advisor screens use False, the main screen True.
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)


	def update(self, fDelta): # called after handleInput
		pass


	def handleInput(self, inputClass):
		if inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED:
			screen = self.getScreen()
			iIndex = screen.getSelectedPullDownID(self.GAMESPEED_DROPDOWN_ID)
			iGameSpeed = screen.getPullDownData(self.GAMESPEED_DROPDOWN_ID, iIndex)
			gc.getInitCore().setGameSpeed(iGameSpeed)
		return 1 # Consume all inputs

	# Could perhaps also handle the simulated key presses here. Would have to remember in which way the screen was closed, and CvGlobals::simulateKeyPressed would have to be exposed to Python for specific keys. (Because figuring out the Windows key codes in Python would require some contortions I think. We might then as well try to trigger the key presses directly from Python via the ctypes module.)
	'''
	def onClose(self):
		gc.simulateTabKeyPressed()
		gc.simulateReturnKeyPressed()
	'''
