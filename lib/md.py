class MardownFile: 

    def __init__(self): 
        self.content = []

    def __add_content(self,element):
        self.content.append(element)
        return element

    def format_img(self,desc,url): 
        return f"![{desc}]({url})"

    def format_quote(self,element): 
        return f"```{element}```"

    def format_array_row(self,*args):
        return f"|{'|'.join(args)}|"

    def add_title(self,element):
        return self.__add_content(f"# {element}")

    def add_section(self,element):
        return self.__add_content(f"## {element}")

    def add_subsection(self,element):
        return self.__add_content(f"### {element}")

    def add_element(self,element):
        return self.__add_content(f"{element}")

    def add_element_quote(self,element):
        return 

    def add_new_line(self):
        return self.__add_content("")

    def add_image(self,desc,url):
        return self.format_img(desc,url)

    def add_array_header(self,headers_name):
        length = len(headers_name)
        header = self.format_array_row(*headers_name)
        seperator = self.format_array_row(*length*["----"])
        content = self.__add_content(header)
        content += self.__add_content(seperator)
        return content 
    def add_array_row(self,*args): 
        content = self.format_array_row(*args)
        return self.__add_content(content)

    def write(self,path_file):
        with open(path_file, "w") as text_file:
            text_file.write("\n".join(self.content))