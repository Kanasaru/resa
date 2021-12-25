###[Resa docs](../../index.md) > [CodeRef Index](../index.md) > [forms.label](forms.label.md) > [forms.label.Label](#forms.label.Label)

## forms.label.Label

form object that reperesents a text label and can be used in [forms.title.Title]().<br>
`Label(position) -> Label`<br>
`Label(position, text) -> Label`<br>
`Label(position, text, font_size) -> Label`<br>
`Label(position, text, font_size, callback) -> Label`<br>

&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.pos_x](#forms.label.Label.pos_x)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Gets or sets the horizontal position.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.pos_y](#forms.label.Label.pos_y)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Gets or sets the vertical position.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.text](#forms.label.Label.text)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Gets or sets the displayed text.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.font](#forms.label.Label.font)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Gets or stes the font object.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.font_size](#forms.label.Label.font_size)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Gets or sets the font size.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.font_colors](#forms.label.Label.font_colors)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Gets or sets the font colors.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.callback](#forms.label.Label.callback)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Gets or sets the callback function.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.LEFT](#forms.label.Label.LEFT)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Const for left alignment.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.RIGHT](#forms.label.Label.RIGHT)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Const for right alignment.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.CENTER](#forms.label.Label.CENTER)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Const for center alignment.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.image](#forms.label.Label.image)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Gets or sets the surface.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.rect](#forms.label.Label.rect)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Gets or sets the rect of the surface.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.alignment](#forms.label.Label.alignment)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Gets or sets the default alignment.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.sprite_sheet_handler](#forms.label.Label.sprite_sheet_handler)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Gets or sets the sprite sheet handler instance.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.set_font](#forms.label.Label.set_font())<br>
&nbsp;&nbsp;&nbsp;&nbsp;Sets the font of the label.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.render_text](#forms.label.Label.render_text())<br>
&nbsp;&nbsp;&nbsp;&nbsp;Renders text on the image.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.font_color](#forms.label.Label.font_color())<br>
&nbsp;&nbsp;&nbsp;&nbsp;Sets the font color of the displayed text.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.update](#forms.label.Label.update())<br>
&nbsp;&nbsp;&nbsp;&nbsp;Updates the label by return value of the callback.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.set_alpha](#forms.label.Label.set_alpha())<br>
&nbsp;&nbsp;&nbsp;&nbsp;Sets the alpha of the label surface.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.set_colorkey](#forms.label.Label.set_colorkey())<br>
&nbsp;&nbsp;&nbsp;&nbsp;Sets the colorkey of the label surface.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.handle_event](#forms.label.Label.handle_event())<br>
&nbsp;&nbsp;&nbsp;&nbsp;Handles given event.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.get_dimensions](#forms.label.Label.get_dimensions())<br>
&nbsp;&nbsp;&nbsp;&nbsp;Returns form dimensions.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.width](#forms.label.Label.width())<br>
&nbsp;&nbsp;&nbsp;&nbsp;Returns form width.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.height](#forms.label.Label.height())<br>
&nbsp;&nbsp;&nbsp;&nbsp;Returns form height.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.align](#forms.label.Label.align())<br>
&nbsp;&nbsp;&nbsp;&nbsp;Aligns the form horizontally in relation to its own position.<br>

### Attributes and Methods

####forms.label.Label.pos_x

####forms.label.Label.pos_y

####forms.label.Label.text

####forms.label.Label.font

####forms.label.Label.font_size

####forms.label.Label.font_colors

####forms.label.Label.callback

####forms.label.Label.LEFT

####forms.label.Label.RIGHT

####forms.label.Label.CENTER

####forms.label.Label.image

#### forms.label.Label.rect

####forms.label.Label.alignment

####forms.label.Label.sprite_sheet_handler

####forms.label.Label.set_font()

####forms.label.Label.render_text()

####forms.label.Label.font_color()

####forms.label.Label.update()

####forms.label.Label.set_alpha()

####forms.label.Label.set_colorkey()

####forms.label.Label.handle_event()

####forms.label.Label.get_dimensions()

####forms.label.Label.width()

####forms.label.Label.height()

####forms.label.Label.align()

### Events

### Exceptions


    data.forms.label.Label

Initializes a label form object. Inherites from `Form()`.

**data.forms.label.Label**
```python
Label(self, position: tuple[int, int],
      text: str = "", font_size: int = conf.std_font_size,
      callback=None) -> None:
```

- `position` position of the textbox on the title
- `text` displayed text
- `font_size` font size of displayed text
- `callback` callback function which is called on update

## Attributes
- pos_x = `position[0]`
- pos_y = `position[1]`
- text = `text`
- font = None
- font_size = `font_size`
- font_colors = {"standard": conf.COLOR_BLACK,}
- callback = `callback`

## Methods