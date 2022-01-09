**[Resa docs](../../index.md) > [CodeRef Index](../index.md) > [world.grid](grid.md) > [world.grid.Grid](#worldgridgrid)**

## world.grid.Grid

object that reperesents a grid<br>
`Grid(fields_x, fields_y, grid) -> Grid`<br>

&nbsp;&nbsp;&nbsp;&nbsp;[world.grid.Grid.fields_x](#fields_x)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Represents the number of grid fields on x-axis.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[world.grid.Grid.fields_y](#fields_y)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Represents the number of grid fields on y-axis<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[world.grid.Grid.width](#width)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Represents the width of a grid field.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[world.grid.Grid.height](#height)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Represents the height of a grid field.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[world.grid.Grid.iso_width](#iso_width)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Represents the width of an isometric grid field.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[world.grid.Grid.iso_height](#iso_height)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Represents the height of an isometric grid field.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[world.grid.Grid.grid_width](#grid_width)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Represents the grids width.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[world.grid.Grid.grid_height](#grid_height)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Represents the grids height.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[world.grid.Grid.fields](#fields)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Holds all grid fields.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[world.grid.Grid.fields_iso](#fields_iso)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Holds all isometric grid fields.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[world.grid.Grid.calc_grid](#calc_grid)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Calculates the normal grid and fills the grid field dictionary.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[world.grid.Grid.draw_grid](#draw_grid)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Draws the normal grid onto given surface.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[world.grid.Grid.pos_in_grid_field](#pos_in_grid_field)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Checks if given position is in grid and returns the grid field as GridField.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[world.grid.Grid.calc_iso_grid](#calc_iso_grid)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Calculates the isometric grid and fills the isometric grid field dictionary.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[world.grid.Grid.draw_iso_grid](#draw_iso_grid)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Draws the isometric grid onto given surface.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[world.grid.Grid.pos_in_iso_grid_field](#pos_in_iso_grid_field)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Checks if given position is in isometric grid and returns the grid field as GridField.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[world.grid.Grid.area_of_triangle](#area_of_triangle)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Calculates the area of a triangle.<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[world.grid.Grid.is_in_triangle](#is_in_triangle)<br>
&nbsp;&nbsp;&nbsp;&nbsp;Checks if a point is in a triangle, which is created by given points.<br><br>

### Attributes and Methods

#### fields_x
Represents the number of grid fields on x-axis.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`fields_x -> int`

#### fields_y
Represents the number of grid fields on y-axis<br>
&nbsp;&nbsp;&nbsp;&nbsp;`fields_y -> int`

#### width
Represents the width of a grid field.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`width -> int`

#### height
Represents the height of a grid field.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`height -> int`

#### iso_width
Represents the width of an isometric grid field.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`iso_width -> int`

#### iso_height
Represents the height of an isometric grid field.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`iso_height -> int`

#### grid_width
Represents the grids width.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`grid_width -> int`

#### grid_height
Represents the grids height.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`grid_height -> int`

#### fields
Holds all grid fields.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`fields -> dict[GridField]`

#### fields_iso
Holds all isometric grid fields.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`fields_iso -> dict[GridField]`

#### calc_grid()
Calculates the normal grid and fills the grid field dictionary.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`calc_grid() -> None`

#### draw_grid()
Draws the normal grid onto given surface.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`draw_grid(surface) -> None`<br>
&nbsp;&nbsp;&nbsp;&nbsp;`draw_grid(surface, position) -> None`<br>
&nbsp;&nbsp;&nbsp;&nbsp;`draw_grid(surface, position, color) -> None`<br>

#### pos_in_grid_field()
Checks if given position is in grid and return the grid field as GridField.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`pos_in_grid_field(point) -> GridField`<br><br>
Given point is checked against a grid with a position on (0, 0). Point has to be normalized.

#### calc_iso_grid()
Calculates the isometric grid and fills the isometric grid field dictionary.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`calc_iso_grid() -> None`

#### draw_iso_grid()
Draws the isometric grid onto given surface.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`draw_iso_grid(surface) -> None`<br>
&nbsp;&nbsp;&nbsp;&nbsp;`draw_iso_grid(surface, position) -> None`<br>
&nbsp;&nbsp;&nbsp;&nbsp;`draw_iso_grid(surface, position, color) -> None`<br>

#### pos_in_iso_grid_field()
Checks if given position is in isometric grid and return the grid field as GridField.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`pos_in_iso_grid_field(point) -> GridField`<br><br>
Given point is checked against a grid with a position on (0, 0). Point has to be normalized.

#### area_of_triangle()
Calculates the area of a triangle.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`area_of_triangle(x1, y1, x2, y2, x3, y3) -> float`

#### is_in_triangle()
Checks if a point is in a triangle, which is created by given points.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`is_in_triangle(x1, y1, x2, y2, x3, y3, x, y) -> bool`

### Events

Raises and handles no events.

### Exceptions

Raises no exceptions.