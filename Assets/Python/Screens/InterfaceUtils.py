# lfgr 09/2019
from CvPythonExtensions import *

import BugCore
import BugUtil
import CvUtil


gc = CyGlobalContext()
BugOpt = BugCore.game.Advisors
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()


def updateMinimap( *args ) :
	"""
	Re-draws the minimap
	"""
	CyMap().updateMinimapColor()


def font( font, text ) :
	return u"<font=%s>%s</font>" % ( font, text )


def makeTableColWidths( wTotal, lfWeights ) :
	wTotal -= 5 * ( len( lfWeights ) - 1 ) # Column separators (?)
	fTotalWeight = sum( lfWeights )
	
	wUsed = 0
	for fWeight in lfWeights[:-1] :
		wCol = int( wTotal * fWeight / fTotalWeight )
		wUsed += wCol
		yield wCol
	
	yield wTotal - wUsed # Last column


def addMessage( ePlayer, szMessage, bForce = True, iLength = None, szSound = "",
		eType = InterfaceMessageTypes.MESSAGE_TYPE_INFO, szIcon = None, eFlashColor = ColorTypes.NO_COLOR,
		iFlashX = -1, iFlashY = -1, bShowOffScreenArrows = False, bShowOnScreenArrows = False ) :
	""" Like CyInterface().addMessage, but with default arguments, and the szMessage argument moved. """
	if iLength is None :
		iLength = gc.getEVENT_MESSAGE_TIME()
	CyInterface().addMessage( ePlayer, bForce, iLength, szMessage, szSound, eType, szIcon, eFlashColor, iFlashX,
			iFlashY, bShowOffScreenArrows, bShowOnScreenArrows )


def setTableColHeaders( screen, szTable, wTable, lfWeights, lszHeaders = None ) :
	if lszHeaders is None :
		lszHeaders = [""] * len( lfWeights )
	for i, wCol in enumerate( makeTableColWidths( wTable, lfWeights ) ) :
		screen.setTableColumnHeader( szTable, i, lszHeaders[i], wCol )
	


def addTableRow( screen, szTable, lszCellText, leCellAlignments = None ) :
	iRow = screen.appendTableRow( szTable )
	
	if isinstance( lszCellText, str ) or isinstance( lszCellText, unicode ) : # Allow lszCellText to be a single string
		lszCellText = [lszCellText]
	
	if leCellAlignments is None : # Everything left-aligned by default
		leCellAlignments = [CvUtil.FONT_LEFT_JUSTIFY] * len( lszCellText )
	
	for iCol, szText in enumerate( lszCellText ) :
		screen.setTableText( szTable, iCol, iRow, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1,
				leCellAlignments[iCol] )

# lfgr 09/2019: Full-screen Advisors
class GenericAdvisorScreen( object ) :
	"""
	Generic Advisor screen class with with helper functions, in particular for full-screen advisors.
	"""
	
	EXIT_ID = "Exit"
	
	def getScreen( self ) :
		raise NotImplementedError( "Subclasses of GenericAdvisor must implement getScreen()" )
	
	def initDimensions( self ) :
		screen = self.getScreen()
		
		if BugOpt.isFullScreenAdvisors() and screen.getXResolution() > 1024 :
			self.wScreen = max( 1024, screen.getXResolution() )
			self.hScreen = max( 720, screen.getYResolution() )
			screen.setDimensions( 0, 0, self.wScreen, self.hScreen )
			BugUtil.debug( "Initializing %s with fulls-screen resolution %dx%d" \
					% ( self.__class__.__name__, self.wScreen, self.hScreen ) )
		else:
			self.wScreen = 1024
			self.hScreen = 768
			screen.setDimensions( screen.centerX(0), screen.centerY(0),
								  self.wScreen, self.hScreen )
			BugUtil.debug( "Initializing %s with normal resolution %dx%d" \
					% ( self.__class__.__name__, self.wScreen, self.hScreen ) )
		
		# Update other dimensions
		self.xExitButton = self.wScreen - 30
		self.yExitButton = self.hScreen - 42
		
		return self.wScreen, self.hScreen # For convenience
	
	def addBackgroundHeaderFooter( self, szHeaderText ) :
		wScreen, hScreen = self.wScreen, self.hScreen
		screen = self.getScreen()
		
		self.hHeader = 55
		self.hFooter = 55
		self.yFooter = hScreen - self.hFooter
		self.yMainArea = self.hHeader
		self.hMainArea = self.hScreen - self.hHeader - self.hFooter
		
		# Background
		screen.addDDSGFC("BackgroundPicture",
				ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(),
				0, 0, wScreen, hScreen, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Header
		screen.addPanel( "TopPanel", u"", u"", True, False, 0, 0, wScreen, self.hHeader,
				PanelStyles.PANEL_STYLE_TOPBAR )
		screen.setLabel( "TitleHeader", "Background", u"<font=4>" + szHeaderText + u"</font>",
				CvUtil.FONT_CENTER_JUSTIFY, wScreen / 2, 8, 0, FontTypes.TITLE_FONT,
				WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Footer
		screen.addPanel( "BottomPanel", u"", u"", True, False, 0, self.yFooter,
				wScreen, self.hFooter, PanelStyles.PANEL_STYLE_BOTTOMBAR )
	
	def addExitButton( self ) :
		screen = self.getScreen()
		
		szExitText = CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper()
		screen.setText( self.EXIT_ID, "Background", u"<font=4>" + szExitText + "</font>",
				CvUtil.FONT_RIGHT_JUSTIFY, self.xExitButton, self.yExitButton, 0,
				FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setActivation( self.EXIT_ID, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )

