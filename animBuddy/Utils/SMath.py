class SMath(object):

    @staticmethod
    def fit2RangeVal( vMin, vMax, pMin, pMax, pos):
        #get 1% of pos range
        pos_percent = float(pMax - pMin) / float(vMax - vMin) # 2.5
        
        val = (pos - 10) / float(pos_percent)

        val = vMin + val

        #return int(round(val,0))
        return float(round(val, 3))

    @staticmethod
    def fit2RangePos( vMin, vMax, pMin, pMax, val):

        #get 1% of pos range
        pos_percent = (pMax - pMin) / 100.0

        #get 1% of val range
        val_percent = (vMax - vMin) / 100.0

        # what val % in range {vMin, vMax}
        abs_value = abs(vMin) + val
        abs_value_percentage = abs_value / float(val_percent)

        # get pos % in range {pMin, pMax} knowing value percentage
        pos_percentage = pMin + pos_percent * abs_value_percentage

        #return int(pos_percentage)
        return float(pos_percentage)

    @staticmethod
    def fit2RangeValInt( vMin, vMax, pMin, pMax, pos):
        #get 1% of pos range
        pos_percent = float(pMax - pMin) / float(vMax - vMin) # 2.5
        
        val = (pos - 10) / float(pos_percent)

        val = vMin + val

        return int(round(val,0))

    @staticmethod
    def fit2RangePosInt( vMin, vMax, pMin, pMax, val):

        #get 1% of pos range
        pos_percent = (pMax - pMin) / 100.0

        #get 1% of val range
        val_percent = (vMax - vMin) / 100.0

        # what val % in range {vMin, vMax}
        abs_value = abs(vMin) + val
        abs_value_percentage = abs_value / float(val_percent)

        # get pos % in range {pMin, pMax} knowing value percentage
        pos_percentage = pMin + pos_percent * abs_value_percentage

        return int(pos_percentage)