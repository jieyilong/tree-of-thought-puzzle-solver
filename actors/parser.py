import numpy as np
import common.utils as utils
import common.consts as consts

class LLMReplyParserBase(object):

    def __init__(self) -> None:
        pass

    def parse_llm_reply(self, llm_reply):
        pass


class LLMReplyParserForSudoku(LLMReplyParserBase):

    def __init__(self) -> None:
        pass

    def parse_llm_reply(self, llm_reply):
        success, json_obj = utils.extract_json_from_text_string(llm_reply)

        if not success:
            return False, None
        
        if not (consts.KEY_ROWS in json_obj):
            return False, None
        
        rows = json_obj[consts.KEY_ROWS]
        
        # rectify the cells
        rectified_rows = []
        for row in rows:
            rectified_row = []
            for cell in row:
                rectified_cell = None
                if cell == None or str(cell).lower() == "none" or str(cell).lower() == "null":
                    rectified_cell = "*"
                else:
                    rectified_cell = str(cell)
                rectified_row.append(rectified_cell)
            rectified_rows.append(rectified_row)
        solution = np.matrix(rectified_rows)

        return True, solution
