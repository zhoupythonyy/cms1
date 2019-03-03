﻿var vm = new Vue({
    el: '#app',
    data: {
        host: 'http://127.0.0.1:8000',
        goods_list: [],         // 购物车中的商品
        origin_input: 1,        // 商品数量
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
    },

    computed: {
        select_all: function() {
            for (let i = 0; i < this.goods_list.length; i++) {
                let goods = this.goods_list[i];
                // 重新计算小计金额, 自动刷新界面显示
                if (!goods.selected) {
                    return false;
                }
            }
            return true;
        },

        // 获取选中的商品的数量
        selected_count: function() {
            let total_count = 0;
            for (let i = 0; i < this.goods_list.length; i++) {
                let goods = this.goods_list[i];
                // 重新计算小计金额, 自动刷新界面显示
                goods.amount = parseFloat(goods.sell_price) * parseInt(goods.count);
                if (goods.selected) {
                    total_count += parseInt(goods.count);
                }
            }
            return total_count;
        },

        // 获取选中的商品的总金额
        selected_amount: function() {
            let total_amount = 0;
            for (let i = 0; i < this.goods_list.length; i++) {
                let goods = this.goods_list[i];
                if (goods.selected) {
                    total_amount += parseFloat(goods.sell_price) * parseInt(goods.count);
                }
            }
            // 金额保存两位有效数字
            return total_amount.toFixed(2);
        },
    },

    mounted: function () {
        this.get_cart_goods();
    },

    methods: {
        // 全选和全不选
        on_select_all: function() {
            let select = !this.select_all;
            for (let i = 0; i < this.goods_list.length; i++) {
                this.goods_list[i].selected = select;
            }
        },

        // 获取购物车商品数据
        get_cart_goods: function () {
           //发送请求
            axios.get(this.host + '/cart/', {
                headers: {  // 传递登录状态jwt
                    'Authorization': 'JWT ' + this.token
                },
            })
                .then(response =>{
                    this.goods_list = response.data
                })
                .catch(error =>{
                    console.log(error)
                })
        },

        // 点击增加购买数量
        on_add: function(index) {
            let goods = this.goods_list[index];
            let count = parseInt(goods.count) + 1;

            this.update_cart_count(goods.id, count, index);
        },

        // 点击减少购买数量
        on_minus: function(index){
            let goods = this.goods_list[index];
            let count = parseInt(goods.count);
            if (count > 1) {
                count--;
                this.update_cart_count(goods.id, count, index);
            }
        },

        // 更新购物车商品购买数量
        on_input: function(index) {
            // 输入的数量不能超过最大库存
            let goods = this.goods_list[index];
            this.update_cart_count(goods.id, goods.count, index);
        },

        // 更新购物车商品数量
        update_cart_count: function(goods_id, count, index) {
            //发送请求
            axios.put(this.host + '/cart/', {
                goods_id:goods_id,
                count:count,
                index:index
            }, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }})
                .then(response => {
                    this.goods_list[index].count = response.data.count;
                })
                .catch(error=>{
                    console.log(error)
                })

        },

        // 删除购物车中的一个商品
        delete_goods: function(index){
            //发送请求
            var config = {
                data: {  // 注意：delete方法参数的传递方式
                    goods_id: this.goods_list[index].id
                },
                headers:{
                    'Authorization': 'JWT ' + this.token
                },};
            axios.delete(this.host + '/cart/', config)
                .then(response =>{
                    this.goods_list.splice(index, 1);
                })
                .catch(error =>{
                    console.log(error)
                })


        },

        // 清空购物车
        clearCart: function(index){
            //发送请求
        },
    }
});