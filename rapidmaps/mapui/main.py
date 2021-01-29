import re
from pathlib import Path

from wx import BG_STYLE_PAINT, Exit, AutoBufferedPaintDC as abDC

from rapidmaps.mapui.wxui.generated.rapidmap import MainFrame
from rapidmaps.map.state import MapStateType
from rapidmaps.map.shape import *
from rapidmaps.map.meta import MapHistoryLoader, MapHistoryWriter, Map
from rapidmaps.map.base import RapidMap
from rapidmaps.map.object import MapToObjectTransformator, MapObjectWriter
from rapidmaps.core.zip_utils import extract_map_name, extract_map_name_no_execpt,\
    MapFileException, MapFileNotExistException

from rapidmaps.map.workflow.init import IconInitWF, ShapeInitWF, HistoryInitWF
from rapidmaps.map.workflow.canvas import CanvasClickWF, WFCanvasClickEvent, WFCanvasClickEventType


def remove_from_list(shape, a_list: list):
    a_list.remove(shape)


class RapidMapFrame(MainFrame):

    def __init__(self):
        super().__init__(None)
        self._appconfig = wx.GetApp().app_conf
        self.canvas.SetBackgroundStyle(BG_STYLE_PAINT)
        self._map = RapidMap(self.canvas, self._appconfig)
        self._map_history = MapHistoryLoader(self._appconfig.conf_path).load()
        self._shape_lib = self._map.shape_lib

        self._selections = self._map.selections
        self._ms = self._map.mapstate
        self._mst = self._map.mapstatetranslator
        self._shape_lib_groups = {}
        self._cur_shape_btn = None
        self._cur_action_btn = self.m_move_btn
        self._all_shape_btns = {}

        ShapeInitWF(self).process()
        IconInitWF(self).process()
        HistoryInitWF(self).process()

        self._click_wf = CanvasClickWF(self)

    @property
    def map(self):
        return self._map

    @property
    def map_history(self):
        return self._map_history

    @property
    def cur_shape_btn(self):
        return self._cur_shape_btn

    @cur_shape_btn.setter
    def cur_shape_btn(self, new_current_shape_btn):
        self._cur_shape_btn = new_current_shape_btn

    @property
    def redraw_left_navigation_pane_complete(self):
        return self._redraw_left_navigation_pane_complete

    @property
    def shape_lib(self):
        return self._shape_lib

    @property
    def shape_lib_groups(self):
        return self._shape_lib_groups

    @property
    def all_shape_btns(self):
        return self._all_shape_btns

    @property
    def recalc_map_list_size(self):
        return self._recalc_map_list_size

    @property
    def edit_enabled(self):
        return self.__edit_enabled

    @property
    def set_edit_by(self):
        return self.__set_edit_by

    def on_left_navi_resize_done(self, event):
        self._recalc_map_list_size()

    def _recalc_map_list_size(self):
        list_size = self.m_splitter1.GetSashPosition() - self.m_splitter1.GetSashSize() - 15
        self.m_map_history_list.SetMaxSize(wx.Size(list_size, 150))
        self.m_map_history_list.SetColumnWidth(0, list_size)

    def _redraw_left_navigation_pane_complete(self):
        b_pos = self.m_splitter1.GetSashPosition()
        self.m_splitter1.SetSashPosition(b_pos + 1)
        self.m_splitter1.SetSashPosition(b_pos)

    def on_mode_change_toggle(self, event):
        self._cur_action_btn.SetValue(not self._cur_action_btn != event.EventObject)
        self._cur_action_btn = event.EventObject

        self._ms.set(MapStateType.MOVING_MODE_UI, self._cur_action_btn == self.m_move_btn)
        self._ms.set(MapStateType.SELECTION_MODE_UI, self._cur_action_btn == self.m_select_btn)
        self._ms.set(MapStateType.ADDITION_MODE_UI, self._cur_action_btn == self.m_add_btn)
        self.m_shape_lib.Enable(enable=self.should_add_entity())

    def OnShapeChange(self, event):
        event.Skip()

    def canvasOnLeftDown(self, event):
        self._click_wf.process(WFCanvasClickEvent(WFCanvasClickEventType.LEFT_MOUSE_DOWN, event))

    def canvasOnMotion(self, event):
        self._ms.set(MapStateType.MOUSE_POS, event.Position)
        if self._mst.is_selection_area_active:
            self.canvas.Refresh()
        elif self._mst.selection_is_moving:
            self._ms.set(MapStateType.SELECTION_IS_MOVING, True)

            self._map.move_selected_shapes()
        else:
            self._ms.set(MapStateType.SELECTION_IS_MOVING, False)

    def canvasOnLeftUp(self, event):
        self._click_wf.process(WFCanvasClickEvent(WFCanvasClickEventType.LEFT_MOUSE_UP, event))

    def _canvas_set_key(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_CONTROL:
            self._ms.set(MapStateType.KB_CTRL, event.EventType)
        elif keycode == wx.WXK_ALT:
            self._ms.set(MapStateType.KB_ALT, event.EventType)
        elif keycode == wx.WXK_SHIFT:
            self._ms.set(MapStateType.KB_SHIFT, event.EventType)

    def canvasOnKeyDown(self, event):
        self._canvas_set_key(event)
        event.Skip()

    def canvasOnKeyUp(self, event):
        self._canvas_set_key(event)
        event.Skip()

    def canvasOnPaint(self, event):
        dc = abDC(self.canvas)
        self._map.update(dc)

    def _adjust_scrollbars(self):
        scroll = self._map.get_update_scrollbar_dimensions()
        hsbar, vsbar = scroll.horizontal, scroll.vertical
        self.m_map_hscroll.SetScrollbar(hsbar.pos, hsbar.thumb_size, hsbar.max_pos, hsbar.page_size, True)
        self.m_map_vscroll.SetScrollbar(vsbar.pos, vsbar.thumb_size, vsbar.max_pos, vsbar.page_size, True)

    def should_add_entity(self):
        return self._ms.get(MapStateType.ADDITION_MODE_UI).value

    def OnLoadMap(self, event):
        if self._map.map_object and self._map.map_object.background.image and \
                wx.MessageBox("Do you really want to reload the Map?", "Please confirm",
                                             wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
            event.Skip()
        else:
            with wx.FileDialog(self, "Open Map file",
                               wildcard="PNG,JPEG,JPG files (*.png;*.jpeg;*.jpg)|*.png;*.jpeg;*.jpg",
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    event.Skip()
                else:
                    try:
                        pathname = fileDialog.GetPath()
                        self._map.set_background(Path(pathname))
                        self._adjust_scrollbars()
                        self.m_zoom.Value = 100
                    except IOError:
                        wx.LogError("Cannot open file '%s'." % pathname)

    def OnClose(self, event):
        self.__process_exit()

    def OnExit(self, event):
        self.__process_exit()

    def __process_exit(self):
        dlg = wx.MessageDialog(self,
                               "Do you want to close the Editor?",
                               'Closing Rapid Map Editor',
                               wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            writer = MapHistoryWriter(self._appconfig.conf_path)
            writer.write(self._map_history)
            Exit()

    def canvasOnSize(self, event):
        self._map.do_resize_viewport(event.Size)
        if self._map.map_object:
            self._adjust_scrollbars()

    def OnClearMap(self, event):
        if self._map.map_object and self._map.map_object.shape_obj:
            self._map.map_object.shape_obj.clear()
            self.canvas.Refresh()

    def OnRemoveSelected(self, event):
        if not self._selections.is_empty():
            self._selections.action(remove_from_list, [self._map.map_object.shape_obj])
            self._selections.clear()
            self.canvas.Refresh()

    def OnNameChanged(self, event):
        if not self._selections.is_empty():
            self._selections.action_on('set_name', [event.String])
            self.canvas.Refresh()

    def OnSizeChanged(self, event):
        if not self._selections.is_empty():
            self._selections.action_on('set_size', [Size(event.Int, event.Int)])
            self.canvas.Refresh()

    def OnTextSizeChanged(self, event):
        if not self._selections.is_empty():
            self._selections.action_on('set_text_size', [event.Int])
            self.canvas.Refresh()

    def OnRotationChanged(self, event):
        if not self._selections.is_empty():
            self._selections.action_on('set_angle', [event.Int])
            self.canvas.Refresh()

    def OnColourChanged(self, event):
        if not self._selections.is_empty():
            self._selections.action_on('set_color', [event.Colour])
            self.canvas.Refresh()

    def __edit_enabled(self, enabled: bool):
        self.m_name.Enable(enabled)
        self.m_size.Enable(enabled)
        self.m_colour.Enable(enabled)
        self.m_rotation.Enable(enabled)
        self.m_text_size.Enable(enabled)

    def __set_edit_by(self, shape: Shape):
        self.m_name.SetValue(shape.get_name())
        self.m_size.SetValue(shape.get_size().x)
        self.m_colour.SetColour(shape.get_color())
        self.m_rotation.SetValue(shape.get_angle())
        self.m_text_size.SetValue(shape.get_text_size())

    def _do_zoom(self, zoom_value: int):
        if self._map.map_object and self._map.map_object.background.image:
            self._map.do_zoom(zoom_value)
            self._adjust_scrollbars()

    def OnMapZoom(self, event):
        self._do_zoom(event.Int)

    def m_map_hscrollOnScroll(self, event):
        # todo only repaint until realtim scroll is enabled(should be added)
        self._map.view.viewport.base.x = event.Position
        self.canvas.Refresh()

    def m_map_vscrollOnScroll(self, event):
        #todo only repaint until realtim scroll is enabled(should be added)
        self._map.view.viewport.base.y = event.Position
        self.canvas.Refresh()

    def canvasOnMouseWheel(self, event):
        if event.controlDown:
            wheeldiff = 0.1 if event.shiftDown else 0.01
            new_val = self.m_zoom.Value + (event.WheelRotation*wheeldiff)
            self.m_zoom.Value = min(max(new_val, self.m_zoom.Min), self.m_zoom.Max)
            self._do_zoom(self.m_zoom.Value)

    def on_map_add_new(self, event):
        #TODO cleanup: First do ist work then do it right ;)
        with wx.TextEntryDialog(self, "Enter new Map's Name") as newMapDialog:
            if newMapDialog.ShowModal() == wx.ID_CANCEL:
                event.Skip()
            else:
                new_map_name = newMapDialog.GetValue()
                if len(new_map_name) > 0:
                    self.m_map_history_list.InsertItem(0, new_map_name)
                    zip_file_name = re.sub(r"\W", "_", new_map_name)
                    self._map_history.add(Map(new_map_name, self._appconfig.map_save_path / f"{zip_file_name}.zip"))
                else:
                    wx.MessageDialog(self, "Unusable Map Name!!",
                                     style=wx.OK_DEFAULT | wx.ICON_ERROR).ShowModal()

    def _get_selected_map_name(self):
        sel_index = self.m_map_history_list.GetFirstSelected()
        if sel_index != -1:
            map_item = self.m_map_history_list.GetItem(sel_index)
            map_name = map_item.GetText()
        return map_name, sel_index

    def _map_edit(self, max_tries: int):
        map_name, _ = self._get_selected_map_name()
        used_map = self._map_history.get(map_name=map_name)
        if self._map.map_object is None or (self._map.map_object and self._map.map_object.map is not used_map):
            try:
                map_obj = MapToObjectTransformator(used_map, self._appconfig.shape_path).transform()
                self._map.map_object = map_obj
            except (MapFileNotExistException, MapFileException) as mfne:
                edit_history = wx.MessageDialog(self, f"Error on open Map: {str(mfne)}.\nEdit History entry?",
                                                caption="Map Open Error", style=wx.YES_NO | wx.ICON_ERROR).ShowModal()
                if edit_history == wx.ID_YES and max_tries > 0:
                    max_tries = max_tries - 1
                    with wx.FileDialog(self, "Select history Map File",
                                       wildcard="ZIP files (*.zip)|*.zip",
                                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as mapImportDialog:

                        if mapImportDialog.ShowModal() == wx.ID_OK:
                            pathname = mapImportDialog.GetPath()
                            if map_name == extract_map_name_no_execpt(pathname):
                                used_map.archive_path = Path(pathname)
                                self._map_edit(max_tries)
                            else:
                                wx.MessageDialog(self, "Map File not match history", caption="Map Open Error",
                                                                style=wx.OK_DEFAULT | wx.ICON_ERROR).ShowModal()

    def on_map_edit(self, event):
        max_tries = 3
        self._map_edit(max_tries)

    def on_map_delete(self, event):
        map_name, sel_index = self._get_selected_map_name()

        with wx.MessageDialog(self, f"Do you want to delete Map \'{map_name}\'?", 'Closing Rapid Map Editor',
                               wx.YES_NO | wx.ICON_QUESTION) as map_del_dlg:

            if map_del_dlg.ShowModal() == wx.ID_YES:
                self._map_history.remove_by_name(map_name)
                self.m_map_history_list.DeleteItem(sel_index)
                self._map.map_object = None
                self.m_map_del_btn.Enable(False)
                self.m_map_edit_btn.Enable(False)
                self.m_map_save_btn.Enable(False)

    def _do_map_save(self):
        MapObjectWriter(self._map.map_object).write()

    def on_map_save(self, event):
        self._do_map_save()

    def on_select_map(self, event):
        self.m_map_del_btn.Enable(True)
        self.m_map_edit_btn.Enable(True)
        self.m_map_save_btn.Enable(True)

    def on_map_import( self, event):
        with wx.FileDialog(self, "Import Existing Map",
                           wildcard="ZIP files (*.zip)|*.zip",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as mapImportDialog:

            if mapImportDialog.ShowModal() == wx.ID_CANCEL:
                event.Skip()
            else:
                pathname = mapImportDialog.GetPath()
                try:
                    imported_map_name = extract_map_name(pathname)
                    self._map_history.add(Map(imported_map_name, Path(pathname)))
                    self.m_map_history_list.InsertItem(0, imported_map_name)
                except MapFileException as mfe:
                    wx.MessageDialog(self, str(mfe), caption="Map Import Error",
                                     style=wx.OK_DEFAULT | wx.ICON_ERROR).ShowModal()

