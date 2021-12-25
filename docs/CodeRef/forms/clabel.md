**[Resa docs](../../index.md) > [CodeRef Index](../index.md) > [forms.label](label.md) > [forms.label.Label](#formslabellabel)**

## forms.label.Label

form object that reperesents a text label<br>
`Label(position) -> Label`<br>
`Label(position, text) -> Label`<br>
`Label(position, text, font_size) -> Label`<br>
`Label(position, text, font_size, callback) -> Label`<br>

&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.pos_x](#pos_x)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Gets or sets the horizontal position.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.pos_y](#pos_y)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Gets or sets the vertical position.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.text](#text)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Gets or sets the displayed text.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.font](#font)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Gets or stes the font object.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.font_size](#font_size)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Gets or sets the font size.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.font_colors](#font_colors)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Gets or sets the font colors.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.callback](#callback)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Gets or sets the callback function.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.set_font](#set_font)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Sets the font of the label.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.render_text](#render_text)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Renders text on the image.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.font_color](#font_color)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Sets the font color of the displayed text.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[forms.label.Label.update](#update)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Updates the label by return value of the callback.<br>

The _Label_ class represents a text surface that can be used directly or as a form object in [forms.title.Title](). It inherits from [forms.form.Form]() and partly overrides its methods.

### Attributes and Methods

#### pos_x

Gets or sets the horizontal position.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`pos_x -> int`

#### pos_y

Gets or sets the vertical position.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`pos_y -> int`

#### text

Gets or sets the displayed text.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`text -> str`

#### font

Gets or stes the font object.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`font -> pygame.font.Font`

#### font_size

Gets or sets the font size.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`font_size -> int`

#### font_colors

Gets or sets the font colors.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`font_colors -> dict`<br><br>
Only used key is `'standard'` and has [conf.COLOR_BLACK]() as default value.

#### callback

Gets or sets the callback function.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`callback -> function`<br><br>

#### set_font()

Sets the font of the label.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`set_font(font) -> None`<br>
&nbsp;&nbsp;&nbsp;&nbsp;`set_font(False) -> None`<br>
&nbsp;&nbsp;&nbsp;&nbsp;`set_font(font, size) -> None`<br>
&nbsp;&nbsp;&nbsp;&nbsp;`set_font(False, size) -> None`<br><br>
Creates a pygame.font.Font or a pygame.font.SysFont reference and calls [render_text()](#render_text) to render the font. The font has to be a string or False. If it is False a system font is uses. The size can be any integer bigger or equal 0.

#### render_text()

Renders text on the image.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`render_text() -> None`

#### font_color()

Sets the font color of the displayed text.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`font_color(color) -> None`<br><br>
Color has to be a Tuple(int, int, int).

#### update()

Updates the label by return value of the callback.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`update() -> None`<br><br>
If callback is set it updates, renders and aligns the text.

### Events

Raises and handles no events.

### Exceptions

Raises no exceptions.