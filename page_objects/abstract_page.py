class AbstractPage:
    DEFAULT_TIMEOUT = 25
    LOAD_TIMEOUT = 60
    LONG_LOAD_TIMEOUT = 100
    BATCH_LOADER_TIMEOUT = 240
    PROGRESS_BAR_TIMEOUT = 60
    TITLE_TIMEOUT = 45
    SHORT_TIME = 1
    LOADER_TIME = 2
    MIDDLE_TIME = 3
    LONG_TIME = 5
    MAX_STALE_REFERENCE_OCCURRENCE = 100
    STABILITY_CHART_LOADING = 9999
    BODY = (By.XPATH, '//html//body')
    REFRESH_CHART_CIRCLE = (
    By.XPATH, '//span[contains(@class, "glyphicon glyphicon-refresh glyphicon-refresh-animate")]')
    CIRCLE_PROGRESS_LOADER = (By.XPATH, '//div[@class="process-step-overlay"]')
    SPINNER = (By.XPATH, '//div[contains(@class, "spinner")]')
    BULK_APPROVAL_LOADER = (By.XPATH, '//div[@style="display: block;"]/div[@class="chart-loader"]')

    def __init__(self, driver):
        self.driver = driver
        self.ALERT = None

    def wait_for_loader(self):
        self.wait_for_disappear(self.REFRESH_CHART_CIRCLE, self.LONG_LOAD_TIMEOUT)
        self.wait_for_disappear(self.CIRCLE_PROGRESS_LOADER)
        self.wait_for_disappear(self.SPINNER)

    # region NAVIGATION
    def open(self, url):
        self.driver.get(url)

    def open_new_tab(self):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])

    def go_home(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.HOME)
        actions.perform()

    def go_bottom(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.END)
        actions.perform()

    def press_enter(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ENTER)
        actions.perform()

    def press_arrow(self, arrow):
        if 'RIGHT' in arrow:
            k = Keys.ARROW_RIGHT
        elif 'LEFT' in arrow:
            k = Keys.ARROW_LEFT
        actions = ActionChains(self.driver)
        actions.send_keys(k)
        actions.perform()

    def clear_all(self):
        key = Keys.COMMAND if ('darwin' in platform().lower() or 'mac' in platform().lower()) \
            else Keys.CONTROL
        ActionChains(self.driver).key_down(key).send_keys('a').key_up(key).perform()
        self.press_backspace()

    def hard_refresh(self):
        self.driver.refresh()
        self.wait_for_long_load()

    def click_holding_ctrl_button_down(self, elements, values):
        key = Keys.COMMAND if ('darwin' in platform().lower() or 'mac' in platform().lower()) \
            else Keys.CONTROL
        actions = ActionChains(self.driver)
        actions.key_down(key)
        if len(values) == 1:
            actions.click(values)
        else:
            for i in values:
                actions.click(i)
        actions.key_up(key)
        actions.perform()

    # endregion

    # region INTERACTIONS
    def clear(self, locator):
        self.find_element(locator).clear()

    def clear_by_js(self, locator):
        self.set_element_value(locator, "")

    def click_by_text(self, text):
        from selenium.webdriver.common.by import By
        locator = (By.XPATH, f'//*[text()="{text}"]')
        self.click(locator)

    def click_body(self):
        self.click(self.BODY)

    def type_without_element(self, text):
        actions = ActionChains(self.driver)
        actions.send_keys(text)
        actions.perform()

    def press_backspace(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.BACKSPACE)
        actions.perform()

    def type_into(self, locator, value):
        if value is not None:
            self.find_element(locator).send_keys(value)

    def clear_without_losing_focus(self, locator):
        input_value = self.get_attribute_value(locator, 'value')
        if input_value is not None:
            for _ in range(len(input_value)):
                self.find_element(locator).send_keys(Keys.BACKSPACE)

    def set_element_value(self, locator, value):
        element = self.find_element(locator)
        self.driver.execute_script(f"arguments[0].value='{value}';", element)

    def hide_element(self, locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].style.visibility='hidden';", element)

    def hide_webelement(self, webelement):
        self.driver.execute_script("arguments[0].style.visibility='hidden';", webelement)

    def hold_and_scroll(self, locator, pixels=50):
        element = self.find_element(locator)
        actions = ActionChains(self.driver)
        actions.click_and_hold(element)
        actions.move_by_offset(0, pixels)
        actions.release()
        actions.perform()

    def scroll_into_view(self, element):
        if isinstance(element, tuple):
            element = self.find_element(element)
        self.driver.execute_script('arguments[0].scrollIntoView({behavior: "smooth", block: "end"});', element)
        self.driver.execute_script('arguments[0].scrollIntoView({behavior: "smooth", block: "center"});', element)

    def scroll_into_view_without_smooth(self, element):
        element = self.find_element(element)
        self.driver.execute_script('arguments[0].scrollIntoView({block: "end"});', element)
        self.driver.execute_script('arguments[0].scrollIntoView({block: "center"});', element)

    def scroll_into_element(self, selector):
        self.driver.execute_script("jQuery('" + selector + "').get(0).scrollIntoView({behavior: 'smooth'});")

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo({top: 0, left: document.body.scrollHeight, behavior: 'smooth'})")

    def scroll_to_bottom(self):
        self.driver.execute_script(
            "window.scrollBy({top: document.body.scrollHeight || document.documentElement.scrollHeight, left: 0, behavior: 'smooth'})")

    def click_by_js(self, element):
        if isinstance(element, tuple):
            element = self.find_element(element)
        cnt = 0
        while cnt < self.MAX_STALE_REFERENCE_OCCURRENCE:
            try:
                self.driver.execute_script('arguments[0].click();', element)
                break
            except StaleElementReferenceException:
                cnt += 1

    def click(self, locator):
        cnt = 0
        flag = True
        while flag and cnt <= self.MAX_STALE_REFERENCE_OCCURRENCE:
            try:
                element = self.wait_for_clickable(locator)
                if 'firefox' in self.driver.name:
                    self.scroll_into_view(element)
                    self.move_to(locator)
                    self.find_element(locator).click()
                else:
                    ActionChains(self.driver).move_to_element(element).click(element).perform()
                flag = False
            except (StaleElementReferenceException, NoSuchElementException, TimeoutException) as e:
                sleep(0.2)
                cnt += 1
                if self.MAX_STALE_REFERENCE_OCCURRENCE == cnt:
                    raise e

        # self.soft_wait_for_load()

    def click_by_element(self, webelement):
        if 'firefox' in self.driver.name:
            self.scroll_into_view(webelement)
            ActionChains(self.driver).click(webelement).perform()
        else:
            clicker = ActionChains(self.driver).move_to_element(webelement)
            clicker.click(webelement)
            clicker.perform()
        self.wait_for_load()

    def hover_and_click(self, locator):
        action = ActionChains(self.driver)
        element = self.find_element(locator)
        action.move_to_element(element).perform()
        return element.click()

    def set_text_in_dropdown(self, dropdown_locator, text):
        Select(self.find_element(dropdown_locator)).select_by_visible_text(text)

    def hover_by_locator(self, locator):
        webelement = self.find_element(locator)
        self.hover_by_element(webelement)

    def hover_by_element(self, element):
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()

    def drag_and_drop(self, source, target):
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    def drag_and_drop_by_locator(self, source_locator, target_locator):
        cnt = 0
        while cnt <= self.MAX_STALE_REFERENCE_OCCURRENCE:
            try:
                self.drag_and_drop(self.find_element(source_locator), self.find_element(target_locator))
                break
            except StaleElementReferenceException as e:
                cnt += 1
                sleep(0.3)
                if cnt == self.MAX_STALE_REFERENCE_OCCURRENCE:
                    raise e

    def move_to_element_with_offset(self, locator, xoffset=0, yoffset=0):
        if isinstance(locator, tuple):
            locator = self.find_element(locator)
        with ActionChains(self.driver) as ac:
            ac.move_to_element_with_offset(locator, xoffset, yoffset).perform()

    def move_to_element_with_offset_and_delay(self, locator, xoffset=0, yoffset=0):
        if isinstance(locator, tuple):
            locator = self.find_element(locator)
        with ActionChains(self.driver) as ac:
            ac.pause(0.5).move_to_element_with_offset(locator, xoffset, yoffset).perform()

    def move_to_element_by_coordinates(self, locator, xoffset=0, yoffset=0):
        if isinstance(locator, tuple):
            locator = self.find_element(locator)
        el_x = locator.location_once_scrolled_into_view['x']
        el_y = locator.location_once_scrolled_into_view['y']
        self.wait_for_load()
        with ActionChains(self.driver) as ac:
            ac.move_to_element_with_offset(self.find_element(self.BODY), el_x + xoffset, el_y + yoffset).perform()

    def move_to_element_with_offset_and_click(self, locator, xoffset=0, yoffset=0):
        if isinstance(locator, tuple):
            locator = self.find_element(locator)
        ActionChains(self.driver).move_to_element_with_offset(locator, xoffset=xoffset,
                                                              yoffset=yoffset).click().perform()

    def move_to_element_with_offset_and_double_click(self, element, xoffset=0, yoffset=0):
        if isinstance(element, tuple):
            element = self.find_element(element)
        ActionChains(self.driver).move_to_element_with_offset(element, xoffset=xoffset,
                                                              yoffset=yoffset).double_click().perform()

    def move_to(self, locator):
        if isinstance(locator, tuple):
            locator = self.find_element(locator)
        act = ActionChains(self.driver).move_to_element(locator)
        act.perform()

    def move_to_with_delay(self, locator):
        if isinstance(locator, tuple):
            locator = self.find_element(locator)
        ''' sleep for geckodriver only'''
        with ActionChains(self.driver) as ac:
            ac.pause(0.75).move_to_element(locator).perform()

    def react_drag_and_drop(self, source, target):
        # IT'S WORKAROUND FOR REACT DRAG&DROP NOT SURE WHY, BUT PAUSES ARE NECESSARY. DON'T REMOVE THEM!
        act = ActionChains(self.driver).click_and_hold(source)
        act.pause(0.1)
        act.move_by_offset(-10, 0)
        act.move_to_element(target)
        act.pause(0.1)
        act.release()
        act.perform()

    def select_alert_option(self, option):
        option = option.upper()
        if self.ALERT is None:
            self.ALERT = self.driver.switch_to.alert
        if 'CANCEL' in option:
            self.ALERT.dismiss()
        else:
            self.ALERT.accept()
            sleep(self.MIDDLE_TIME)

    def approve_alert_by_click_enter(self):
        if self.ALERT is None:
            self.ALERT = self.driver.switch_to.alert
        self.ALERT.send_keys(Keys.RETURN)

    def remove_duplicates_from_list(self, data):
        data_set = set()
        data_add = data_set.add
        return [x for x in data if not (x in data_set or data_add(x))]
    # endregion

    # region WAITS

    def wait_for_text_in_locator(self, locator, text, timeout=DEFAULT_TIMEOUT):
        cnt = 0
        while cnt < timeout * 10:
            try:
                current_text = self.get_text(locator, timeout=self.SHORT_TIME)
                if current_text is None or text not in current_text:
                    cnt += 1
                else:
                    return
            except (TimeoutException, StaleElementReferenceException, NoSuchElementException):
                cnt += 1

    def wait_for_disappear(self, locator, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout=timeout).until_not(EC.visibility_of_all_elements_located(locator))

    def wait_for_clickable(self, element_locator, timeout=SHORT_TIME):
        return WebDriverWait(self.driver, timeout=timeout).until(EC.element_to_be_clickable(element_locator))

    def wait_for_enabled(self, element_locator, timeout=DEFAULT_TIMEOUT):
        count = 0
        while self.find_element(element_locator).get_attribute("disabled") == 'disabled':
            sleep(0.25)
            count += 1
            if count >= timeout * 4:
                raise Exception(f"Element is not enabled.\n Locator:{element_locator}")

    def wait_for_alert(self, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout=timeout).until(EC.alert_is_present())

    @staticmethod
    def wait_for_element_visible(web_element=None, timeout=DEFAULT_TIMEOUT):
        count = 0
        while not web_element.is_displayed():
            sleep(0.25)
            count += 1
            if count >= timeout * 4:
                raise NoSuchElementException()

    def wait_for_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        cnt = 0
        while cnt <= self.MAX_STALE_REFERENCE_OCCURRENCE:
            try:
                element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_any_elements_located(locator))
                return element
            except StaleElementReferenceException:
                cnt += 1
            except TimeoutException as e:
                raise e

    def wait_for_presence_of(self, locator, timeout=DEFAULT_TIMEOUT):
        cnt = 0
        while cnt <= self.MAX_STALE_REFERENCE_OCCURRENCE:
            try:
                element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
                return element
            except StaleElementReferenceException:
                cnt += 1
            except TimeoutException as e:
                raise e

    def wait_for_remove(self, locator, timeout=DEFAULT_TIMEOUT):
        cnt = 0
        flag = True
        while cnt < timeout * 4 and flag:
            try:
                self.find_element(locator)
                sleep(0.25)
                cnt += 1
            except NoSuchElementException:
                flag = False

    def wait_for_element_enabled(self, webelement, timeout=DEFAULT_TIMEOUT):
        ActionChains(self.driver).move_to_element(webelement)
        count = 0
        while not webelement.is_enabled():
            sleep(0.25)
            count += 1
            if count >= timeout * 4:
                raise NoSuchElementException()

    def wait_for_url(self, url, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout=timeout).until(EC.url_contains(url))

    def wait_for_any_element_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout=timeout).until(EC.visibility_of_any_elements_located(locator))

    def wait_for_presence_of_element_located(self, locator, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout=timeout).until(EC.presence_of_element_located(locator))

    def wait_for_redirect(self, timeout=DEFAULT_TIMEOUT):
        cnt = 0
        flag = True
        while flag and cnt < timeout * 5:
            try:
                self.wait_for_visible(self.BODY)
                flag = False
            except WebDriverException:
                sleep(0.2)
                cnt += 1

    def wait_for_load(self, timeout=LOAD_TIMEOUT):
        WebDriverWait(self.driver, timeout=timeout) \
            .until(lambda x: x.execute_script('return document.readyState=="complete" && jQuery.active==0'))

    def wait_for_long_load(self, timeout=LONG_LOAD_TIMEOUT):
        WebDriverWait(self.driver, timeout=timeout) \
            .until(lambda x: x.execute_script('return document.readyState=="complete" && jQuery.active==0'))

    def soft_wait_for_load(self):
        WebDriverWait(self.driver, timeout=self.DEFAULT_TIMEOUT) \
            .until(lambda x: x.execute_script('return document.readyState=="complete" && jQuery.active==0'))

    def wait_for_ajax(self):
        self.driver.execute_script("var callback = arguments[arguments.length - 1];"
                                   "var xhr = new XMLHttpRequest();"
                                   "xhr.open('GET', '/Ajax_call', true);"
                                   "xhr.onreadystatechange = function() {if (xhr.readyState == 4) "
                                   "{callback(xhr.responseText);}};xhr.send();")

    # endregion

    # region FINDINGS
    def find_visible_element(self, locator):
        return self.find_visible_element_in_list(self.find_elements(locator))

    @staticmethod
    def find_visible_element_in_list(elements_list):
        for x in elements_list:
            if x.is_displayed():
                return x
        return None

    def find_visible_elements(self, locator: object) -> object:
        return [x for x in self.find_elements(locator) if x.is_displayed()]

    @staticmethod
    def find_parent(element, grade):
        element_to_return = element.find_element_by_xpath("..")
        for x in range(0, grade - 2):
            element_to_return = element_to_return.find_element_by_xpath("..")
        return element_to_return

    @staticmethod
    def find_elements_in_element(element, locator):
        return element.find_elements(*locator)

    @staticmethod
    def find_element_in_element(element, locator):
        return element.find_element(*locator)

    def find_elements(self, locator, timeout=LONG_TIME):
        try:
            self.wait_for_any_element_visible(locator, timeout=timeout)
        except (TimeoutException, StaleElementReferenceException):
            pass
        return self.driver.find_elements(*locator)

    def find_invisible_elements(self, locator):
        return self.driver.find_elements(*locator)

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def find_element_by_text(self, text):
        from selenium.webdriver.common.by import By
        locator = (By.XPATH, f'//*[text()="{text}"]')
        return self.find_element(locator)

    @staticmethod
    def get_element_from_list_by_text(elements_list, text):
        for x in elements_list:
            if text in x.text:
                return x
        return None

    def find_options_of_dropdown(self, locator):
        return Select(self.find_element(locator)).options

    def get_attribute_value(self, locator, attribute):
        self.wait_for_any_element_visible(locator)
        element = self.find_element(locator)
        return element.get_attribute(attribute)

    def find_selected_options_of_dropdown(self, locator):
        self.wait_for_any_element_visible(locator)
        select = Select(self.find_element(locator))
        selected_options = select.all_selected_options
        return selected_options

    def find_single_selected_option_of_dropdown(self, locator):
        return self.find_selected_options_of_dropdown(locator)[0].text

    # endregion

    # region READING DATA
    def get_alert_text(self):
        if self.ALERT is None:
            self.ALERT = self.driver.switch_to.alert
        try:
            txt = self.ALERT.text
        except TimeoutException:
            txt = None
        return txt

    def get_tooltip(self, locator):
        data_title = self.get_attribute_value(locator, 'data-original-title')
        if data_title is not None and len(data_title) > 0:
            return data_title
        else:
            return self.get_attribute_value(locator, 'title')

    def get_inner_text(self, locator):
        return self.find_element(locator).get_attribute('innerText')

    def get_validation_message(self, locator):
        return self.find_element(locator).get_attribute("validationMessage")

    def get_data_from_table(self, title_locator, table_locator):
        self.scroll_into_view(table_locator)
        data_table = self.find_visible_element(table_locator).get_attribute('innerHTML').replace('<th></th>', '')
        soup = BeautifulSoup(data_table, 'lxml')
        data_rows = soup.find_all('tr')
        rows_values_scrap = [[td.getText() for td in data_rows[i].findAll('td')]
                             for i, v in enumerate(data_rows)]
        rows_values = [x for x in rows_values_scrap if x]
        columns_scrap = [[td.getText() for td in data_rows[i].findAll('th')]
                         for i, v in enumerate(data_rows)]
        columns = [x for x in columns_scrap if x]
        table = []
        if columns[0][0] == 'Model':
            columns[0].pop(0)
        if columns[1:] != []:
            for i, r in enumerate(columns[1:]):
                table.append(
                    [f'column: {columns[0][j]}, row_title: {columns[1:][i][0]}, cell: {rows_values[i][j]}' for j, c in
                     enumerate(columns[0])])
        elif len(columns) == 1:
            if rows_values:
                for i, v in enumerate(rows_values):
                    table.append([f'column: {columns[0][j]}, cell: {rows_values[i][j]}' for j, c in enumerate(columns[0])])
            else:
                table.append([f'column: {header}' for header in columns[0]])

        else:
            table.append([f'column: {columns[0][j]}, cell: {rows_values[0][j]}' for j, c in enumerate(columns[0]) if
                          columns[1:] == []])
        table.insert(0, f'title: {self.find_visible_element(title_locator).text}')
        return table

    @staticmethod
    def get_element_validation_message(element):
        return element.get_attribute("validationMessage")

    def get_text(self, locator, timeout=DEFAULT_TIMEOUT):
        try:
            self.wait_for_visible(locator, timeout=timeout)
            return self.find_element(locator).text
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            return None

    def get_text_from_elements(self, list_locator):
        elements = self.find_elements(list_locator)
        return [element.text for element in elements if len(element.text) > 0]

    def get_driver(self):
        return self.driver

    def get_current_url(self):
        return self.driver.current_url

    def get_page_source(self):
        return self.driver.page_source

    def get_color(self, locator):
        color = self.find_element(locator).value_of_css_property("color")
        return self.color_parser(color)

    def get_element_color(self, webelement):
        return self.color_parser(webelement.value_of_css_property("color"))

    def get_element_background_color(self, webelement):
        return self.color_parser(webelement.value_of_css_property("background-color"))

    def get_background_color(self, locator):
        color = self.find_element(locator).value_of_css_property("background-color")
        return self.color_parser(color)

    def color_parser(self, color):
        if "rgba" in color:
            rgb = tuple(int(c) for c in color.replace("rgba", "").replace("(", "").replace(")", "").split(','))
            x = '#{:02x}{:02x}{:02x}{:02x}'.format(*rgb)
        elif "rgb" in color:
            rgb = tuple(int(c) for c in color.replace("rgb", "").replace("(", "").replace(")").split(','))
            x = '#{:02x}{:02x}{:02x}'.format(*rgb)
        return x

    def date_converter(self, values):
        set_date = (set(values).intersection(list_of_dates()))
        return [list_of_dates_as_dict().get("".join(set_date)) if v == "".join(set_date) else v for v in values]

    def date_converter_in_string(self, string):
        chart_date = str(datetime.now().strftime('%d-%b-%Y'))
        if chart_date in string:
            a = f"{string.split(',')[0]}, current date"
            if len(string.split(',')[1]) > 19:
                try:
                    b = string.split(',')[1].rsplit('|', 1)[1]
                except IndexError:
                    b = string.split(',')[1].rsplit('-', 1)[1]
                a = f'{a},{b}'
            return a
        else:
            return string

    # endregion

    # region VALIDATION
    def check_element(self, locator, timeout=LONG_TIME):
        try:
            self.wait_for_visible(locator, timeout=timeout)
            return True
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            return False

    def is_any_element_visible(self, locator):
        for x in self.find_invisible_elements(locator):
            if x.is_displayed():
                return True
            else:
                continue
        return False

    def validate(self, items_to_check):
        if len(items_to_check) == 0:
            return True
        else:
            result = False
            for it in items_to_check:
                result = self.check_element(it)
            return result

    def get_element_inline_style_attribute_value(self, locator, attribute):
        element = self.find_element(locator)
        style = element.get_attribute("style")
        if style is not None:
            return get_inline_style_attribute_value_from_style(attribute, style)
        else:
            return None

    def get_webelement_inline_style_attribute_value(self, webelement, attribute):
        style = webelement.get_attribute("style")
        if style is not None:
            return get_inline_style_attribute_value_from_style(attribute, style)
        else:
            return None

    # endregion

    def switch_to_tab(self, new_tab):
        self.driver.switch_to.window(new_tab)

    def close_tab(self):
        self.driver.close()

    def prepare_download(self):
        from testrunner.utils.path_utils import downloads_dir
        # It's (very) nasty workaround for preparing downloads in headless chrome. It changes all the download links to
        # be open in same tab.
        if 'chrome' in self.driver.name:
            self.driver.execute_script("var x = document.getElementsByTagName('a'); var i; for "
                                       "(i = 0; i < x.length; i++) { x[i].target = '_self'; }")
            self.driver.command_executor._commands["send_command"] = ("POST",
                                                                      '/session/$sessionId/chromium/send_command')
            params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow',
                                                                    'downloadPath': downloads_dir()}}
            self.driver.execute("send_command", params)

    def _select(self, locator, text_to_select_by):
        if isinstance(locator, tuple):
            self.wait_for_any_element_visible(locator)
            self.scroll_into_view(locator)
            select = Select(self.find_element(locator))
        else:
            self.scroll_into_view(locator)
            select = Select(locator)
        select.select_by_visible_text(text_to_select_by)
