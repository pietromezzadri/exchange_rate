class Converter:
    def convert_dates_str(self, date_list):
        date_str_list = []
        for date in date_list:
            date_str_list.append(date.strftime("%Y-%m-%d"))
        return date_str_list

    def convert_number_float(self, number_list):
        number_float_list = []
        for number in number_list:
            number_float_list.append(float("{:.3f}".format(number)))
        return number_float_list
