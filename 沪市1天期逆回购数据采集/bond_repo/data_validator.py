class DataValidator:
    @staticmethod
    def validate(data):
        """
        验证数据有效性
        :param data: API返回的数据列表
        :return: (is_valid, error_message)
        """
        # 基本验证：字段数量
        if not data or len(data) < 10:
            return False, "数据字段不足（至少需要 10 个字段）"
            
        # 字段类型验证
        try:
            # 价格字段（浮点数）
            float(data[1])  # current_price
            float(data[2])  # open_price
            float(data[3])  # close_price
            float(data[4])  # high_price
            float(data[5])  # low_price
            float(data[6])  # bid_price
            float(data[7])  # ask_price
            
            # 交易量字段（浮点数，支持科学计数法）
            float(data[8])  # deal_amount
            float(data[9])  # buy_amount
            float(data[10])  # sell_amount
        except (ValueError, IndexError) as e:
            return False, f"数据类型错误: {str(e)}"
            
        # 数值范围验证
        if not (0 <= float(data[1]) <= 100):  # current_price
            return False, "当前价格超出合理范围（0-100）"
            
        if float(data[8]) < 0 or float(data[9]) < 0 or float(data[10]) < 0:  # 交易量
            return False, "交易量不能为负数"
            
        return True, "数据有效"