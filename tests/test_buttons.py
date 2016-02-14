import pytest
import pypush2.buttons

class TestButtons:
  ### Tests for buttons.is_display_button

  def test_is_display_button_first_bottom_button(self):
    button = pypush2.buttons.Buttons.bottom_display_0
    assert pypush2.buttons.is_display_button(button) == True

  def test_is_display_button_last_bottom_button(self):
    button = pypush2.buttons.Buttons.bottom_display_7
    assert pypush2.buttons.is_display_button(button) == True

  def test_is_display_button_first_top_button(self):
    button = pypush2.buttons.Buttons.top_display_0
    assert pypush2.buttons.is_display_button(button) == True

  def test_is_display_button_last_top_button(self):
    button = pypush2.buttons.Buttons.top_display_7
    assert pypush2.buttons.is_display_button(button) == True

  def test_is_display_button_out_of_range_below_bottom(self):
    button = pypush2.buttons.Buttons.bottom_display_0 - 1
    assert pypush2.buttons.is_display_button(button) == False

  def test_is_display_button_out_of_range_above_bottom(self):
    button = pypush2.buttons.Buttons.bottom_display_7 + 1
    assert pypush2.buttons.is_display_button(button) == False

  def test_is_display_button_out_of_range_below_top(self):
    button = pypush2.buttons.Buttons.top_display_0 - 1
    assert pypush2.buttons.is_display_button(button) == False
  
  def test_is_display_button_out_of_range_above_top(self):
    button = pypush2.buttons.Buttons.top_display_7 + 1
    assert pypush2.buttons.is_display_button(button) == False


  ### Tests for buttons.get_display_button_group

  def test_get_group_first_bottom_button(self):
    button = pypush2.buttons.Buttons.bottom_display_0
    assert pypush2.buttons.get_display_button_group(button) == pypush2.buttons.DisplayButtonGroups.bottom

  def test_get_group_last_bottom_button(self):
    button = pypush2.buttons.Buttons.bottom_display_7
    assert pypush2.buttons.get_display_button_group(button) == pypush2.buttons.DisplayButtonGroups.bottom

  def test_get_group_first_top_button(self):
    button = pypush2.buttons.Buttons.top_display_0
    assert pypush2.buttons.get_display_button_group(button) == pypush2.buttons.DisplayButtonGroups.top

  def test_get_group_last_top_button(self):
    button = pypush2.buttons.Buttons.top_display_7
    assert pypush2.buttons.get_display_button_group(button) == pypush2.buttons.DisplayButtonGroups.top

  def test_get_group_out_of_range_below_bottom(self):
    button = pypush2.buttons.Buttons.bottom_display_0 - 1
    with pytest.raises(IndexError):
      pypush2.buttons.get_display_button_group(button)

  def test_get_group_out_of_range_above_bottom(self):
    button = pypush2.buttons.Buttons.bottom_display_7 + 1
    with pytest.raises(IndexError):
      pypush2.buttons.get_display_button_group(button)

  def test_get_group_out_of_range_below_top(self):
    button = pypush2.buttons.Buttons.top_display_0 - 1
    with pytest.raises(IndexError):
      pypush2.buttons.get_display_button_group(button)
  
  def test_get_group_out_of_range_above_top(self):
    button = pypush2.buttons.Buttons.top_display_7 + 1
    with pytest.raises(IndexError):
      pypush2.buttons.get_display_button_group(button)
      

  ### Tests for buttons.get_display_button_index

  def test_get_index_bottom(self):
    button = pypush2.buttons.Buttons.bottom_display_3
    assert pypush2.buttons.get_display_button_index(button) == 3

  def test_get_index_top(self):
    button = pypush2.buttons.Buttons.top_display_5
    assert pypush2.buttons.get_display_button_index(button) == 5

  def test_get_index_out_of_range_below_bottom(self):
    button = pypush2.buttons.Buttons.bottom_display_0 - 1
    with pytest.raises(IndexError):
      pypush2.buttons.get_display_button_index(button)

  def test_get_index_out_of_range_above_bottom(self):
    button = pypush2.buttons.Buttons.bottom_display_7 + 1
    with pytest.raises(IndexError):
      pypush2.buttons.get_display_button_index(button)

  def test_get_index_out_of_range_below_top(self):
    button = pypush2.buttons.Buttons.top_display_0 - 1
    with pytest.raises(IndexError):
      pypush2.buttons.get_display_button_index(button)

  def test_get_index_out_of_range_above_top(self):
    button = pypush2.buttons.Buttons.top_display_7 + 1
    with pytest.raises(IndexError):
      pypush2.buttons.get_display_button_index(button)
