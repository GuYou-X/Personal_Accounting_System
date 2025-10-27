import json
import os
from datetime import datetime

class FinanceManager:
    def __init__(self, data_file="finance_data.json"):
        self.data_file = data_file
        self.transactions = self.load_data()
    
    def load_data(self):
        """加载数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_data(self):
        """保存数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.transactions, f, ensure_ascii=False, indent=2)
    
    def add_transaction(self, data):
        """添加交易记录"""
        transaction = {
            'id': len(self.transactions) + 1,
            'type': data['type'],
            'amount': float(data['amount']),
            'category': data['category'],
            'description': data['description'],
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.transactions.append(transaction)
        self.save_data()
        return transaction
    
    def get_all_transactions(self):
        """获取所有交易记录"""
        return self.transactions
    
    def get_transaction(self, transaction_id):
        """获取单个交易记录"""
        for transaction in self.transactions:
            if transaction['id'] == transaction_id:
                return transaction
        return None
    
    def delete_transaction(self, transaction_id):
        """删除交易记录"""
        self.transactions = [t for t in self.transactions if t['id'] != transaction_id]
        self.save_data()
        return True
    
    def get_statistics(self):
        """获取统计信息"""
        total_income = sum(t['amount'] for t in self.transactions if t['type'] == '收入')
        total_expense = sum(t['amount'] for t in self.transactions if t['type'] == '支出')
        balance = total_income - total_expense
        
        # 支出分类统计
        expense_by_category = {}
        for transaction in self.transactions:
            if transaction['type'] == '支出':
                category = transaction['category']
                amount = transaction['amount']
                expense_by_category[category] = expense_by_category.get(category, 0) + amount
        
        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
            'expense_by_category': expense_by_category
        }
    
    def search_transactions(self, keyword):
        """搜索交易记录"""
        if not keyword:
            return self.transactions
        
        results = []
        for transaction in self.transactions:
            if (keyword.lower() in transaction['category'].lower() or 
                keyword.lower() in transaction['description'].lower()):
                results.append(transaction)
        
        return results