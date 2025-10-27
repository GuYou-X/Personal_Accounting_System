from flask import Flask, request, jsonify
from flask_cors import CORS
from models import FinanceManager

app = Flask(__name__)
CORS(app)  # 允许跨域请求

finance_manager = FinanceManager()

# API路由定义
@app.route('/')
def home():
    return jsonify({"message": "个人记账系统API", "version": "1.0"})

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """获取所有交易记录"""
    transactions = finance_manager.get_all_transactions()
    return jsonify({
        "success": True,
        "data": transactions,
        "count": len(transactions)
    })

@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    """添加交易记录"""
    try:
        data = request.get_json()
        
        # 验证必要字段
        required_fields = ['type', 'amount', 'category']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    "success": False,
                    "message": f"缺少必要字段: {field}"
                }), 400
        
        # 验证类型
        if data['type'] not in ['收入', '支出']:
            return jsonify({
                "success": False,
                "message": "类型必须是'收入'或'支出'"
            }), 400
        
        # 验证金额
        try:
            amount = float(data['amount'])
            if amount <= 0:
                return jsonify({
                    "success": False,
                    "message": "金额必须大于0"
                }), 400
        except ValueError:
            return jsonify({
                "success": False,
                "message": "金额必须是有效数字"
            }), 400
        
        transaction = finance_manager.add_transaction(data)
        return jsonify({
            "success": True,
            "message": "交易记录添加成功",
            "data": transaction
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500

@app.route('/api/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    """删除交易记录"""
    try:
        transaction = finance_manager.get_transaction(transaction_id)
        if not transaction:
            return jsonify({
                "success": False,
                "message": "交易记录不存在"
            }), 404
        
        finance_manager.delete_transaction(transaction_id)
        return jsonify({
            "success": True,
            "message": "交易记录删除成功"
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """获取统计信息"""
    try:
        stats = finance_manager.get_statistics()
        return jsonify({
            "success": True,
            "data": stats
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500

@app.route('/api/search', methods=['GET'])
def search_transactions():
    """搜索交易记录"""
    try:
        keyword = request.args.get('keyword', '')
        results = finance_manager.search_transactions(keyword)
        return jsonify({
            "success": True,
            "data": results,
            "count": len(results)
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)