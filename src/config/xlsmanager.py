'''
Created on 30.08.2013

@author: Based on existing class from <<Python Programming on Win32>>
'''
import win32com.client
from win32com.client import constants  as constants
import os
import traceback
from types import UnicodeType
import copy as copy
#from types import 
 
class easyExcel:
    """A utility to make it easier to get at Excel. Remembering
    to save the data is your problem, as is error handling.
    Operates on one workbook at a time."""

    def __init__(self, filename=None,sheet=None):
        self.xlApp = win32com.client.Dispatch('Excel.Application')
        if filename:
            self.filename = filename
            self.xlBook = self.xlApp.Workbooks.Open(filename)
        else:
            self.xlBook = self.xlApp.Workbooks.Add()
            self.filename = ""
        if sheet:
            self.sheet=sheet
        else:
            self.sheet=""

    def save(self, newfilename=None):
        if newfilename:
            self.filename = newfilename
            self.xlBook.SaveAs(newfilename)
        else:
            self.xlBook.Save()

    def close(self):
        self.xlBook.Close(SaveChanges=0)
        del self.xlApp
    
    def addSheet(self):
        self.xlBook.Worksheets.Add()
    
    def selectSheet(self,sheet_name):
        self.xlBook.Worksheets(sheet_name).Select()   
    
    def hideSheet(self,sheet_name):
        self.xlBook.Worksheets(sheet_name).Visible=False
    
    def copySheet(self,copy_sheet,new_name):
        template_sheet=self.xlBook.Worksheets(copy_sheet)
        #print template_sheet.Name
        #print template_sheet.Index
        
        template_sheet.Copy(None,template_sheet)
        #template_sheet.Copy(None,self.xlBook.Worksheets(copy_sheet)).Name=new_name
        new_sheet_name=copy_sheet+" (2)"
        #print new_sheet_name
        new_sheet=self.xlBook.Worksheets(new_sheet_name)
        new_sheet.Name=new_name
        self.save()
    
    def fillAcrossSheets(self,sheets,origin_sheet,range):    
        #sheets should be a list
        ws = self.selectSheet(origin_sheet)
        ws.Range(range).Formula = "=row()*column()"
        self.xlBook.Worksheets(sheets).FillAcrossSheets(ws.Range(range))
        
    def copyRangeOtherSheet(self,sheet,dict_range,new_sheet,dict_new_range=None):
        if dict_new_range is None:
            dict_new_range=copy.deepcopy(dict_range)
        
        self.selectSheet(sheet)
        ws=self.xlBook.Worksheets(sheet)
        ws.Range(ws.Cells( dict_range['row_start'],dict_range['col_start']),ws.Cells(dict_range['row_end'],dict_range['col_end'])).Select
        ws.Range(ws.Cells(dict_range['row_start'],dict_range['col_start']),ws.Cells(dict_range['row_end'],dict_range['col_end'])).Copy()
        self.selectSheet(new_sheet)
        new_ws=self.xlBook.Worksheets(new_sheet)
        #new_ws.Range(new_ws.Cells(dict_new_range['row_start'],dict_new_range['col_start']),new_ws.Cells(dict_new_range['row_end'],dict_new_range['col_end'])).Select
        new_ws.Cells(dict_new_range['row_start'],dict_new_range['col_start']).Select()
        new_ws.Paste()
    
    def clearRangeContent(self,sheet,dict_range):
        '''Clear contents of desired range'''
        self.selectSheet(sheet)
        ws=self.xlBook.Worksheets(sheet)
        ws.Range(ws.Cells( dict_range['row_start'],dict_range['col_start']),ws.Cells(dict_range['row_end'],dict_range['col_end'])).ClearContents()
        self.save()

    
    def getCell(self,row, col,sheet=None):
        '''Get value of one cell'''
        if sheet is not None:
            sht = self.xlBook.Worksheets(sheet)
        else:
            sht=self.xlBook.Worksheets(self.sheet)
            
        return sht.Cells(row, col).Value

    def setCell(self,row, col, value,sheet=None):
        '''Set value of one cell'''
        if sheet is not None:
            sht = self.xlBook.Worksheets(sheet)
        else:
            sht=self.xlBook.Worksheets(self.sheet)
        sht.Cells(row, col).Value = value

    def getRange(self, sheet, row1, col1, row2, col2):
        '''Return a 2d array (i.e. tuple of tuples)'''
        sht = self.xlBook.Worksheet(sheet)
        return sht.Range(sht.Cells(row1, col1), sht.Cells(row2, col2)).Value    
    
    def setRange(self, sheet, leftCol, topRow, data):
        '''insert a 2d array starting at given location.
        Works out the size needed for itself'''

        bottomRow = topRow + len(data) - 1
    
        rightCol = leftCol + len(data[0]) - 1
        sht = self.xlBook.Worksheets(sheet)
        sht.Range(sht.Cells(topRow, leftCol),sht.Cells(bottomRow, rightCol)).Value = data
    
    def getContiguousRange(self, sheet, row, col):
        '''Tracks down and across from top left cell until it
        encounters blank cells; returns the non-blank range.
        Looks at first row and column; blanks at bottom or right
        are OK and return None within the array'''

        sht = self.xlBook.Worksheets(sheet)
    
        # find the bottom row
        bottom = row
        while sht.Cells(bottom + 1, col).Value not in [None,'']:
            bottom = bottom + 1
    
        # right column
        right = col
        while sht.Cells(row, right + 1).Value not in [None,'']:
            right = right + 1
    
        return sht.Range(sht.Cells(row, col), sht.Cells(bottom, right)).Value
    
    def get_sheet_last_col(self,sheet_name):
        return self.xlBook.Worksheets(sheet_name).UsedRange.Columns.Count
    
    def get_sheet_last_row(self,sheet_name):
        return self.xlBook.Worksheets(sheet_name).UsedRange.Rows.Count
    
    
    def fixStringsAndDates(self, aMatrix):
         # converts all unicode strings and times
         newmatrix = []
         for row in aMatrix:
             newrow = []
             for cell in row:
                 if type(cell) is UnicodeType:
                     newrow.append(str(cell))
                 #elif type(cell) is TimeType:
                 #    newrow.append(int(cell))
                 else:
                     newrow.append(cell)
             newmatrix.append(tuple(newrow))
         return newmatrix

    def convertRCToA1(self, R1C1):
         """
             fromReferenceStyle  =   constants.xlR1C1,
             toReferenceStyle    =   constants.xlA1,
             toabsolute          =   constants.xlRelative)
         """
         return self.xlApp.ConvertFormula(R1C1, constants.xlR1C1,
                                         constants.xlA1, 
                                        constants.xlRelative)

    def insertFormulaInRange(self, sheet, row, col, len, formula):
         self.selectSheet(sheet)
         sht = self.xlBook.Worksheets(sheet)
         sht.Cells(row, col).FormulaR1C1 = formula
         fill_range = sht.Range(sht.Cells(row, col), 
                                sht.Cells(row+len-1, col))
         start = self.convertRCToA1("R"+str(row)+"C"+str(col))
         sht.Range(start).AutoFill(Destination=fill_range)
         
    
    def copyChart(self,sheet,chart_id,new_chart_name):
        self.selectSheet(sheet)
        sht = self.xlBook.Worksheets(sheet)
        sht.ChartObjects(chart_id).Activate()
        chart=sht.ChartObjects(chart_id)
        new_chart=chart.Duplicate()
        new_chart.Name=new_chart_name
        self.save()    
        #chart.ChartArea.Copy()
        #sht.Range(range).Select()
        #sht.Paste()
    
    def refreshWorksheetPivotTables(self,sheet):
        self.selectSheet(sheet)
        sht = self.xlBook.Worksheets(sheet)
        pivot_count = sht.PivotTables().Count
        for i in range(1,pivot_count+1):
            sht.PivotTables(i).PivotCache().Refresh()
            
        self.save()    
        
    
    def refreshUpdatePivotCharts(self,sheet,scaleWth,scaleHht):
        self.selectSheet(sheet)
        sht = self.xlBook.Worksheets(sheet)
        for objChartObject in sht.ChartObjects():
            objChartObject.Activate
            objChartObject.Chart.ChartArea.Select
            chartName = objChartObject.Chart.Parent.Name
            sht.Shapes(chartName).scaleWidth(scaleWth,False,0)  #_msoScaleFromTopLeft
            sht.Shapes(chartName).scaleHeight(scaleHht,False,0) # _msoScaleFromTopLeft
            
        self.save()  
    

    def changeChartLocation(self,sheet_name,chart_name,cell_left_row,cell_left_col,cell_top_row,cell_top_col,range_height,range_width):
        
        self.selectSheet(sheet_name)
        sht = self.xlBook.Worksheets(sheet_name)
        sht.Shapes(chart_name).Left=sht.Cells(cell_left_row,cell_left_col).Left
        sht.Shapes(chart_name).Top=sht.Cells(cell_top_row,cell_top_col).Top
        sht.Shapes(chart_name).Height = sht.Range(range_height).Height
        sht.Shapes(chart_name).Width = sht.Range(range_width).Width
        self.save()
    
    def hideChart(self,sheet,chart_id):
        self.selectSheet(sheet)
        sht = self.xlBook.Worksheets(sheet)
        sht.ChartObjects(chart_id).Visible=False
        
    def changeChartTitle(self,sheet_name,chart_id,chart_name):
        sht = self.xlBook.Worksheets(sheet_name)
        chartproperties = sht.ChartObjects(chart_id).Chart
        chartproperties.ChartTitle.Caption = chart_name
        self.save()
    
    def changeColumnChartData(self,sheet_name,chart_id,range,plot_by=1,sheet_range=None):
        #if plot_by = 1 plot by xlRows,if 2 plot by clColumns
        sht = self.xlBook.Worksheets(sheet_name)
        chartproperties = sht.ChartObjects(chart_id).Chart
        sht.ChartObjects(chart_id).Activate()
        if sheet_range is None:
            chartproperties.SetSourceData(Source=sht.Range(range), PlotBy=plot_by)
        else:
            range_sht = self.xlBook.Worksheets(sheet_range)
            chartproperties.SetSourceData(Source=range_sht.Range(range), PlotBy=plot_by)
        self.save()
    
    
    def changeColumnChartAxisData(self,sheet_name,chart_id,range,plot_by=1,sheet_range=None):
        #if plot_by = 1 plot by xlRows,if 2 plot by clColumns
        sht = self.xlBook.Worksheets(sheet_name)
        chartproperties = sht.ChartObjects(chart_id).Chart
        sht.ChartObjects(chart_id).Activate()
        if sheet_range is None:
           range=sht.Range(range)
        else:
            range = self.xlBook.Worksheets(sheet_range).Range(range)
        chartproperties.SeriesCollection(1).XValues=range
        self.save()

#         se = self.xlChart.Chart.SeriesCollection().NewSeries()
#         se.Values = sht.Range(sht.Cells(topRow,    yCol),
#                                sht.Cells(bottomRow, yCol))
#         se.XValues = sht.Range(sht.Cells(topRow,    xCol),
#                                 sht.Cells(bottomRow, xCol))    
            
            
        self.save()
    
    
    def newChartInSheet(self, sheet, num = 1, left = 10, width = 600,
                             top = 50, height = 450, type = 'xy'):
         if type == 'xy':
            chart_type = constants.xlXYScatter
         try:
             self.selectSheet(sheet)
         except: # sheet doesn't exist so create it
             self.newSheet(sheet)
         try :
             self.xlBook.Sheets(sheet).ChartObjects(num).Activate    # already exists
         except:
             self.xlChart = self.xlBook.Sheets(sheet).ChartObjects().Add(
                                     Left = left, Width = width, Top = top,
                                     Height = height)
             self.xlChart.Chart.ChartType = chart_type

    def addXYChartSeries(self, sheet, topRow, bottomRow, xCol, yCol,
                         series_name="", chart_sheet="", chart_num = 1,
                         color = 1, style = 'line',
                         title = "", xlabel = "", ylabel = "", errorbars = {}):

         if not chart_sheet:
             chart_sheet = sheet

         # series properties
         sht = self.xlBook.Worksheets(sheet)
         se = self.xlChart.Chart.SeriesCollection().NewSeries()
         se.Values = sht.Range(sht.Cells(topRow,    yCol),
                               sht.Cells(bottomRow, yCol))
         se.XValues = sht.Range(sht.Cells(topRow,    xCol),
                                sht.Cells(bottomRow, xCol))
         if series_name:
             se.Name = series_name
         if style == 'line':
             # line style
             se.MarkerStyle = constants.xlNone
             se.Border.ColorIndex = color
             se.Border.Weight = constants.xlHairline
             se.Border.LineStyle = constants.xlContinuous
             se.Border.Weight = constants.xlMedium
         if style == 'point':
             # point style
             #se.MarkerBackgroundColorIndex = constants.xlNone
             #se.MarkerForegroundColorIndex = color
             se.MarkerBackgroundColorIndex = color
             se.MarkerForegroundColorIndex = 1   # black
             #se.MarkerStyle = constants.xlMarkerStyleCircle
             se.MarkerStyle = constants.xlMarkerStyleSquare
             se.MarkerSize = 5
         # Chart properties
         cht = self.xlBook.Sheets(chart_sheet).ChartObjects(chart_num).Chart
         # Chart Title
         if title:
             cht.HasTitle = True
             cht.ChartTitle.Caption = title
             cht.ChartTitle.Font.Name = 'Arial'
             cht.ChartTitle.Font.Size = 10
             cht.ChartTitle.Font.Bold = False
         # X axis labels
         if xlabel:
             cht.Axes(constants.xlCategory).HasTitle = True
             cht.Axes(constants.xlCategory).AxisTitle.Caption = xlabel
             cht.Axes(constants.xlCategory).AxisTitle.Font.Name = 'Arial'
             cht.Axes(constants.xlCategory).AxisTitle.Font.Size = 10
             cht.Axes(constants.xlCategory).AxisTitle.Font.Bold = False
             cht.Axes(constants.xlCategory).MinimumScale = 0
             cht.Axes(constants.xlCategory).MaximumScaleIsAuto = True
         # Y axis labels
         if ylabel:
             cht.Axes(constants.xlValue).HasTitle = True
             cht.Axes(constants.xlValue).AxisTitle.Caption = ylabel
             cht.Axes(constants.xlValue).AxisTitle.Font.Name = 'Arial'
             cht.Axes(constants.xlValue).AxisTitle.Font.Size = 10
             cht.Axes(constants.xlValue).AxisTitle.Font.Bold = False
             cht.Axes(constants.xlValue).MinimumScale = 0
             cht.Axes(constants.xlValue).MaximumScaleIsAuto = True

         if errorbars:
             amount = "".join(["=", chart_sheet, "!",
                                            "R", 
str(errorbars['amount'][0]),
                                            "C", 
str(errorbars['amount'][2]),
                                            ":",
                                            "R", 
str(errorbars['amount'][1]),
                                            "C", 
str(errorbars['amount'][2])])
             se.ErrorBar(Direction = constants.xlY,
                         Include = constants.xlErrorBarIncludeBoth,
                         Type = constants.xlErrorBarTypeCustom,
                         Amount = amount, MinusValues = amount)
             se.ErrorBars.EndStyle = constants.xlNoCap
             se.ErrorBars.Border.LineStyle = constants.xlContinuous
             se.ErrorBars.Border.ColorIndex = color
             se.ErrorBars.Border.Weight = constants.xlHairline
