
$(function(){


  init();

})
function init(){



  var myColor = ['#1089E7', '#F57474', '#56D0E3', '#F8B448', '#8B78F6'];

  //各医院门诊人次
  // var histogramChart1 = echarts.init(document.getElementById('histogramChart1'));
  // histogramChart1.setOption({

  //    grid: {
  //        top: '20%',
  //        left: '32%'
  //    },
  //    xAxis: {
  //        show: false
  //    },
  //    yAxis: [{
  //        show: true,
  //        data:  ['厦门第一医院','厦门中山医院','厦门中医院','厦门第五医院',],
  //        inverse: true,
  //        axisLine: {
  //            show: false
  //        },
  //        splitLine: {
  //            show: false
  //        },
  //        axisTick: {
  //            show: false
  //        },
  //        axisLabel: {
  //            color: '#fff',
  //            formatter: (value, index) => {
  //                return [

  //                    `{lg|${index+1}}  ` + '{title|' + value + '} '
  //                ].join('\n')
  //            },
  //            rich: {
  //                lg: {
  //                    backgroundColor: '#339911',
  //                    color: '#fff',
  //                    borderRadius: 15,
  //                    // padding: 5,
  //                    align: 'center',
  //                    width: 15,
  //                    height: 15
  //                },
  //            }
  //        },


  //    }, {
  //        show: true,
  //        inverse: true,
  //        data: [4000, 3000, 2000, 1000],
  //        axisLabel: {
  //            textStyle: {
  //                fontSize: 12,
  //                color: '#fff',
  //            },
  //        },
  //        axisLine: {
  //            show: false
  //        },
  //        splitLine: {
  //            show: false
  //        },
  //        axisTick: {
  //            show: false
  //        },

  //    }],
  //    series: [{
  //        name: '条',
  //        type: 'bar',
  //        yAxisIndex: 0,
  //        data: [40, 30, 20, 10],
  //        barWidth: 10,
  //        itemStyle: {
  //            normal: {
  //                barBorderRadius: 20,
  //                color: function(params) {
  //                    var num = myColor.length;
  //                    return myColor[params.dataIndex % num]
  //                },
  //            }
  //        },
  //        label: {
  //            normal: {
  //                show: true,
  //                position: 'inside',
  //                formatter: '{c}%'
  //            }
  //        },
  //    }, {
  //        name: '框',
  //        type: 'bar',
  //        yAxisIndex: 1,
  //        barGap: '-100%',
  //        data: [100, 100, 100, 100],
  //        barWidth: 15,
  //        itemStyle: {
  //            normal: {
  //                color: 'none',
  //                borderColor: '#00c1de',
  //                borderWidth: 3,
  //                barBorderRadius: 15,
  //            }
  //        }
  //    }, ]
  // })

  //各医院住院人次
var dom = document.getElementById("table9");
var myChart = echarts.init(dom);
var app = {};
option = null;

myChart.showLoading();

$.get('./life-expectancy.json', function (data) {
    myChart.hideLoading();
option = {
        grid3D: {},
        tooltip: {},
        xAxis3D: {
            type: 'category'
        },
        yAxis3D: {
            type: 'category'
        },
        zAxis3D: {},
        visualMap: {
            max: 1e8,
            dimension: 'Population'
        },
        dataset: {
            dimensions: [
                'Income',
                'Life Expectancy',
                'Population',
                'Country',
                {name: 'Year', type: 'ordinal'}
            ],
            source: data
        },
        series: [
            {
                type: 'bar3D',
                // symbolSize: symbolSize,
                shading: 'lambert',
                encode: {
                    x: 'Year',
                    y: 'Country',
                    z: 'Life Expectancy',
                    tooltip: [0, 1, 2, 3, 4]
                }
            }
        ]
    };

    myChart.setOption(option);

});
if (option && typeof option === "object") {
    myChart.setOption(option, true);
}

//----------------------
app.title = '柱状图框选';

var xAxisData = [];
var data1 = [];
var data2 = [];
var data3 = [];
var data4 = [];

for (var i = 0; i < 10; i++) {
    xAxisData.push('Class' + i);
    data1.push((Math.random() * 2).toFixed(2));
    data2.push(-Math.random().toFixed(2));
    data3.push((Math.random() * 5).toFixed(2));
    data4.push((Math.random() + 0.3).toFixed(2));
}

var itemStyle = {
    normal: {
    },
    emphasis: {
        barBorderWidth: 1,
        shadowBlur: 10,
        shadowOffsetX: 0,
        shadowOffsetY: 0,
        shadowColor: 'rgba(0,0,0,0.5)'
    }
};

option = {
    backgroundColor: '#eee',
    legend: {
        data: ['bar', 'bar2', 'bar3', 'bar4'],
        align: 'left',
        left: 10
    },
    brush: {
        toolbox: ['rect', 'polygon', 'lineX', 'lineY', 'keep', 'clear'],
        xAxisIndex: 0
    },
    toolbox: {
        feature: {
            magicType: {
                type: ['stack', 'tiled']
            },
            dataView: {}
        }
    },
    tooltip: {},
    xAxis: {
        data: xAxisData,
        name: 'X Axis',
        silent: false,
        axisLine: {onZero: true},
        splitLine: {show: false},
        splitArea: {show: false}
    },
    yAxis: {
        inverse: true,
        splitArea: {show: false}
    },
    grid: {
        left: 100
    },
    visualMap: {
        type: 'continuous',
        dimension: 1,
        text: ['High', 'Low'],
        inverse: true,
        itemHeight: 200,
        calculable: true,
        min: -2,
        max: 6,
        top: 60,
        left: 10,
        inRange: {
            colorLightness: [0.4, 0.8]
        },
        outOfRange: {
            color: '#bbb'
        },
        controller: {
            inRange: {
                color: '#2f4554'
            }
        }
    },
    series: [
        {
            name: 'bar',
            type: 'bar',
            stack: 'one',
            itemStyle: itemStyle,
            data: data1
        },
        {
            name: 'bar2',
            type: 'bar',
            stack: 'one',
            itemStyle: itemStyle,
            data: data2
        },
        {
            name: 'bar3',
            type: 'bar',
            stack: 'two',
            itemStyle: itemStyle,
            data: data3
        },
        {
            name: 'bar4',
            type: 'bar',
            stack: 'two',
            itemStyle: itemStyle,
            data: data4
        }
    ]
};

var myChart2 = echarts.init(document.getElementById('table5'));


myChart2.on('brushSelected', renderBrushed);

function renderBrushed(params) {
    var brushed = [];
    var brushComponent = params.batch[0];

    for (var sIdx = 0; sIdx < brushComponent.selected.length; sIdx++) {
        var rawIndices = brushComponent.selected[sIdx].dataIndex;
        brushed.push('[Series ' + sIdx + '] ' + rawIndices.join(', '));
    }

    myChart2.setOption({
        title: {
            backgroundColor: '#333',
            text: 'SELECTED DATA INDICES: \n' + brushed.join('\n'),
            bottom: 0,
            right: 0,
            width: 100,
            textStyle: {
                fontSize: 12,
                color: '#fff'
            }
        }
    });
}
//  var histogramChart2 = echarts.init(document.getElementById('histogramChart2'));

//   $.get('./life-expectancy.json', function (data) {
//     option = {
//         grid3D: {},
//         tooltip: {},
//         xAxis3D: {
//             type: 'category'
//         },
//         yAxis3D: {
//             type: 'category'
//         },
//         zAxis3D: {},
//         visualMap: {
//             max: 1e8,
//             dimension: 'Population'
//         },
//         dataset: {
//             dimensions: [
//                 'Income',
//                 'Life Expectancy',
//                 'Population',
//                 'Country',
//                 {name: 'Year', type: 'ordinal'}
//             ],
//             source: data
//         },
//         series: [
//             {
//                 type: 'bar3D',
//                 // symbolSize: symbolSize,
//                 shading: 'lambert',
//                 encode: {
//                     x: 'Year',
//                     y: 'Country',
//                     z: 'Life Expectancy',
//                     tooltip: [0, 1, 2, 3, 4]
//                 }
//             }
//         ]
//     };
//     histogramChart2.setOption(option);
// });





  // var histogramChart2 = echarts.init(document.getElementById('histogramChart2'));
  // histogramChart2.setOption({

  //    grid: {
  //        top: '20%',
  //        left: '32%'
  //    },
  //    xAxis: {
  //        show: false
  //    },
  //    yAxis: [{
  //        show: true,
  //        data:  ['厦门第一医院','厦门中山医院','厦门中医院','厦门第五医院',],
  //        inverse: true,
  //        axisLine: {
  //            show: false
  //        },
  //        splitLine: {
  //            show: false
  //        },
  //        axisTick: {
  //            show: false
  //        },
  //        axisLabel: {
  //            color: '#fff',
  //            formatter: (value, index) => {
  //                return [

  //                    `{lg|${index+1}}  ` + '{title|' + value + '} '
  //                ].join('\n')
  //            },
  //            rich: {
  //                lg: {
  //                    backgroundColor: '#339911',
  //                    color: '#fff',
  //                    borderRadius: 15,
  //                    // padding: 5,
  //                    align: 'center',
  //                    width: 15,
  //                    height: 15
  //                },
  //            }
  //        },


  //    }, {
  //        show: true,
  //        inverse: true,
  //        data: [2200, 2400, 2600, 2800],
  //        axisLabel: {
  //            textStyle: {
  //                fontSize: 12,
  //                color: '#fff',
  //            },
  //        },
  //        axisLine: {
  //            show: false
  //        },
  //        splitLine: {
  //            show: false
  //        },
  //        axisTick: {
  //            show: false
  //        },

  //    }],
  //    series: [{
  //        name: '条',
  //        type: 'bar',
  //        yAxisIndex: 0,
  //        data:  [22, 24, 26, 28],
  //        barWidth: 10,
  //        itemStyle: {
  //            normal: {
  //                barBorderRadius: 20,
  //                color: function(params) {
  //                    var num = myColor.length;
  //                    return myColor[params.dataIndex % num]
  //                },
  //            }
  //        },
  //        label: {
  //            normal: {
  //                show: true,
  //                position: 'inside',
  //                formatter: '{c}%'
  //            }
  //        },
  //    }, {
  //        name: '框',
  //        type: 'bar',
  //        yAxisIndex: 1,
  //        barGap: '-100%',
  //        data: [100, 100, 100, 100],
  //        barWidth: 15,
  //        itemStyle: {
  //            normal: {
  //                color: 'none',
  //                borderColor: '#00c1de',
  //                borderWidth: 3,
  //                barBorderRadius: 15,
  //            }
  //        }
  //    }, ]
  // })

var pieChart1 = echarts.init(document.getElementById('table4'));
    pieChart1.setOption({
  
 
    title: {
        text: '漏斗图(对比)',
        subtext: '纯属虚构',
        left: 'left',
        top: 'bottom'
    },
    tooltip: {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c}%"
    },
    toolbox: {
        show: true,
        orient: 'vertical',
        top: 'center',
        feature: {
            dataView: {readOnly: false},
            restore: {},
            saveAsImage: {}
        }
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        data: ['产品A','产品B','产品C','产品D','产品E']
    },
    calculable: true,
    series: [
        {
            name: '漏斗图',
            type: 'funnel',
            width: '40%',
            height: '45%',
            left: '5%',
            top: '50%',
            funnelAlign: 'right',

            center: ['25%', '25%'],  // for pie

            data:[
                {value:60, name:'产品C'},
                {value:30, name:'产品D'},
                {value:10, name:'产品E'},
                {value:80, name:'产品B'},
                {value:100, name:'产品A'}
            ]
        },
        {
            name: '金字塔',
            type:'funnel',
            width: '40%',
            height: '45%',
            left: '5%',
            top: '5%',
            sort: 'ascending',
            funnelAlign: 'right',

            center: ['25%', '75%'],  // for pie

            data:[
                {value:60, name:'产品C'},
                {value:30, name:'产品D'},
                {value:10, name:'产品E'},
                {value:80, name:'产品B'},
                {value:100, name:'产品A'}
            ]
        },
        {
            name:'漏斗图',
            type:'funnel',
            width: '40%',
            height: '45%',
            left: '55%',
            top: '5%',
            funnelAlign: 'left',

            center: ['75%', '25%'],  // for pie

            data: [
                {value: 60, name: '产品C'},
                {value: 30, name: '产品D'},
                {value: 10, name: '产品E'},
                {value: 80, name: '产品B'},
                {value: 100, name: '产品A'}
            ]
        },
        {
            name: '金字塔',
            type:'funnel',
            width: '40%',
            height: '45%',
            left: '55%',
            top: '50%',
            sort: 'ascending',
            funnelAlign: 'left',

            center: ['75%', '75%'],  // for pie

            data: [
                {value: 60, name: '产品C'},
                {value: 30, name: '产品D'},
                {value: 10, name: '产品E'},
                {value: 80, name: '产品B'},
                {value: 100, name: '产品A'}
            ]
        }
    ]
});

    // var pieChart1 = echarts.init(document.getElementById('pieChart1'));
    // pieChart1.setOption({
    //   color:["#87cefa","#ff7f50","#32cd32","#da70d6",],
    //   tooltip : {
    //    trigger: 'item',
    //    formatter: "{a}<br/>{b}<br/>{c}台"
    //   },
    //   calculable : true,
    //   series : [
    //       {
    //           name:'手术工作量',
    //           type:'pie',
    //           radius : [30, 110],
    //           center : ['50%', '50%'],
    //           roseType : 'area',
    //           x: '50%',
    //           max: 40,
    //           sort : 'ascending',
    //           data:[
    //               {value:10, name:'厦门第一医院'},
    //               {value:5, name:'厦门中山医院'},
    //               {value:15, name:'厦门中医院'},
    //               {value:25, name:'厦门第五医院'},
    //           ]
    //       }
    //   ]
    // })

    //医疗费用
    // var lineChart1 = echarts.init(document.getElementById('lineChart1'));
    // lineChart1.setOption( {
    //   color:["#87cefa","#ff7f50","#32cd32","#da70d6",],
    //   tooltip : {
    //        trigger: 'item',
    //        formatter: "{a}<br/>{b}<br/>{c}元"
    //    },
    //    legend: {
    //     data:['厦门第一医院','厦门中山医院','厦门中医院','厦门第五医院',],
    //     y: 'bottom',
    //     x:'center',
    //     textStyle:{
    //         color:'#fff',
    //         fontSize:12
    //     }
    //   },
    //   grid:{
    //     left: '5%',
    //     right: '5%',
    //     bottom: '10%',
    //     containLabel: true
    //   },
    //   calculable : true,
    //   xAxis : [
    //       {
    //           type : 'category',
    //           boundaryGap : false,
    //           data : ['周一','周二','周三','周四','周五','周六','周日'],
    //           axisLine:{
    //                lineStyle:{
    //                    color: '#87cefa'
    //                },
    //            },
    //            axisLabel : {
    //              interval:0,
    //              rotate:40,

    //                textStyle: {
    //                    color: '#fff',
    //                    fontSize:13
    //                }
    //            }
    //       }
    //   ],
    //   yAxis : [
    //       {
    //           type : 'value',
    //           axisLine:{
    //               lineStyle:{
    //                   color: '#87cefa'
    //               },
    //           },
    //           splitLine: {
    //               "show": false
    //           },
    //           axisLabel: {
    //               textStyle: {
    //                   color: '#fff'
    //               },
    //               formatter: function (value) {
    //                   return value + "元"
    //               },
    //           },
    //       }
    //   ],
    //   series : [
    //       {
    //           name:'厦门第一医院',
    //           type:'line',
    //           smooth:true,
    //           itemStyle: {normal: {areaStyle: {type: 'default'}}},
    //           data:[10, 12, 21, 54, 260, 830, 710]
    //       },
    //       {
    //           name:'厦门中山医院',
    //           type:'line',
    //           smooth:true,
    //           itemStyle: {normal: {areaStyle: {type: 'default'}}},
    //           data:[30, 182, 434, 791, 390, 30, 10]
    //       },
    //       {
    //           name:'厦门中医院',
    //           type:'line',
    //           smooth:true,
    //           itemStyle: {normal: {areaStyle: {type: 'default'}}},
    //           data:[1320, 1132, 601, 234, 120, 90, 20]
    //       },
    //       {
    //           name:'厦门第五医院',
    //           type:'line',
    //           smooth:true,
    //           itemStyle: {normal: {areaStyle: {type: 'default'}}},
    //           data:[320, 132, 61, 34, 20, 9, 2]
    //       }
    //   ]

    // })

    //体检人次

setTimeout(function () {

    option = {
        legend: {},
        tooltip: {
            trigger: 'axis',
            showContent: false
        },
        dataset: {
            source: [
                ['product', '2012', '2013', '2014', '2015', '2016', '2017'],
                ['Matcha Latte', 41.1, 30.4, 65.1, 53.3, 83.8, 98.7],
                ['Milk Tea', 86.5, 92.1, 85.7, 83.1, 73.4, 55.1],
                ['Cheese Cocoa', 24.1, 67.2, 79.5, 86.4, 65.2, 82.5],
                ['Walnut Brownie', 55.2, 67.1, 69.2, 72.4, 53.9, 39.1]
            ]
        },
        xAxis: {type: 'category'},
        yAxis: {gridIndex: 0},
        grid: {top: '55%'},
        series: [
            {type: 'line', smooth: true, seriesLayoutBy: 'row'},
            {type: 'line', smooth: true, seriesLayoutBy: 'row'},
            {type: 'line', smooth: true, seriesLayoutBy: 'row'},
            {type: 'line', smooth: true, seriesLayoutBy: 'row'},
            {
                type: 'pie',
                id: 'pie',
                radius: '30%',
                center: ['50%', '25%'],
                label: {
                    formatter: '{b}: {@2012} ({d}%)'
                },
                encode: {
                    itemName: 'product',
                    value: '2012',
                    tooltip: '2012'
                }
            }
        ]
    };
 var myChart3 = echarts.init(document.getElementById('table6'));
    myChart.on('updateAxisPointer', function (event) {
        var xAxisInfo = event.axesInfo[0];
        if (xAxisInfo) {
            var dimension = xAxisInfo.value + 1;
            myChart.setOption({
                series: {
                    id: 'pie',
                    label: {
                        formatter: '{b}: {@[' + dimension + ']} ({d}%)'
                    },
                    encode: {
                        value: dimension,
                        tooltip: dimension
                    }
                }
            });
        }
    });

    myChart3.setOption(option);

});
    // var lineChart2 = echarts.init(document.getElementById('table6'));
    // lineChart2.setOption( {
    //   color:["#87cefa","#ff7f50","#32cd32","#da70d6",],
    //   tooltip : {
    //        trigger: 'item',
    //        formatter: "{a}<br/>{b}<br/>{c}人"
    //    },
    //    legend: {
    //     data:['厦门第一医院','厦门中山医院','厦门中医院','厦门第五医院',],
    //     y: 'bottom',
    //     x:'center',
    //     textStyle:{
    //         color:'#fff',
    //         fontSize:12
    //     }
    //   },
    //   grid:{
    //     left: '5%',
    //     right: '5%',
    //     bottom: '10%',
    //     containLabel: true
    //   },
    //   calculable : true,
    //   xAxis : [
    //       {
    //           type : 'category',
    //           boundaryGap : false,
    //           data : ['周一','周二','周三','周四','周五','周六','周日'],
    //           axisLine:{
    //                lineStyle:{
    //                    color: '#87cefa'
    //                },
    //            },
    //            axisLabel : {
    //              interval:0,
    //              rotate:40,

    //                textStyle: {
    //                    color: '#fff',
    //                    fontSize:13
    //                }
    //            }
    //       }
    //   ],
    //   yAxis : [
    //       {
    //           type : 'value',
    //           axisLine:{
    //               lineStyle:{
    //                   color: '#87cefa'
    //               },
    //           },
    //           splitLine: {
    //               "show": false
    //           },
    //           axisLabel: {
    //               textStyle: {
    //                   color: '#fff'
    //               },
    //               formatter: function (value) {
    //                   return value + "人"
    //               },
    //           },
    //       }
    //   ],
    //   series : [
    //       {
    //           name:'厦门第一医院',
    //           type:'line',
    //           smooth:true,
    //           itemStyle: {normal: {areaStyle: {type: 'default'}}},
    //           data:[120, 122, 221, 524, 460, 530, 610]
    //       },
    //       {
    //           name:'厦门中山医院',
    //           type:'line',
    //           smooth:true,
    //           itemStyle: {normal: {areaStyle: {type: 'default'}}},
    //           data:[130, 682, 534, 691, 490, 130, 110]
    //       },
    //       {
    //           name:'厦门中医院',
    //           type:'line',
    //           smooth:true,
    //           itemStyle: {normal: {areaStyle: {type: 'default'}}},
    //           data:[320, 132, 161, 134, 112, 190, 120]
    //       },
    //       {
    //           name:'厦门第五医院',
    //           type:'line',
    //           smooth:true,
    //           itemStyle: {normal: {areaStyle: {type: 'default'}}},
    //           data:[320, 132, 461, 34, 202, 93, 222]
    //       }
    //   ]

    // })

   // 床位数量分布
  // app.title = '极坐标系下的堆叠柱状图';

    var pieChart2 = echarts.init(document.getElementById('table7'));
    pieChart2.setOption({
    angleAxis: {
    },
    radiusAxis: {
        type: 'category',
        data: ['周一', '周二', '周三', '周四'],
        z: 10
    },
    polar: {
    },
    series: [{
        type: 'bar',
        data: [1, 2, 3, 4],
        coordinateSystem: 'polar',
        name: 'A',
        stack: 'a'
    }, {
        type: 'bar',
        data: [2, 4, 6, 8],
        coordinateSystem: 'polar',
        name: 'B',
        stack: 'a'
    }, {
        type: 'bar',
        data: [1, 2, 3, 4],
        coordinateSystem: 'polar',
        name: 'C',
        stack: 'a'
    }],
    legend: {
        show: true,
        data: ['A', 'B', 'C']
    }
});

    // var pieChart2 = echarts.init(document.getElementById('pieChart2'));
    // pieChart2.setOption({
    //   color:["#87cefa","#ff7f50","#32cd32","#da70d6",],
    //   tooltip : {
    //    trigger: 'item',
    //    formatter: "{a}<br/>{b}<br/>{c}床"
    //   },
    //   calculable : true,
    //   series : [
    //       {
    //           name:'床位数量分布',
    //           type:'pie',
    //           radius : [30, 110],
    //           center : ['45%', '50%'],
    //           roseType : 'area',
    //           x: '50%',
    //           max: 40,
    //           sort : 'ascending',
    //           data:[
    //               {value:700, name:'厦门第一医院'},
    //               {value:500, name:'厦门中山医院'},
    //               {value:105, name:'厦门中医院'},
    //               {value:250, name:'厦门第五医院'},
    //           ]
    //       }
    //   ]
    // })

    // //药占比
    // var histogramChart3 = echarts.init(document.getElementById('histogramChart3'));
    // histogramChart3.setOption( {

    //   color:['#87cefa'],
    //   grid:{
    //       left: '5%',
    //       right: '5%',
    //       bottom: '5%',
    //       containLabel: true
    //   },
    //   tooltip : {
    //      trigger: 'item',
    //      formatter: "{a}<br/>{b}<br/>{c}%"
    //  },
    //   calculable : true,
    //   xAxis : [
    //       {
    //           type : 'category',
    //           data : ['厦门第一医院','厦门中山医院','厦门中医院','厦门第五医院',],
    //           axisLine:{
    //                lineStyle:{
    //                    color: '#87cefa'
    //                },
    //            },
    //            axisLabel : {
    //              interval:0,
    //              rotate:40,

    //                textStyle: {
    //                    color: '#fff',
    //                    fontSize:13
    //                }
    //            }
    //       }
    //   ],
    //   yAxis : [
    //       {
    //           type : 'value',
    //           axisLine:{
    //               lineStyle:{
    //                   color: '#87cefa'
    //               },
    //           },
    //           splitLine: {
    //               "show": false
    //           },
    //           axisLabel: {
    //               textStyle: {
    //                   color: '#fff'
    //               },
    //               formatter: function (value) {
    //                   return value + "%"
    //               },
    //           },
    //       }
    //   ],
    //   series : [
    //       {
    //           name:'药占比',
    //           type:'bar',
    //           barWidth:30,
    //           data:[60,80,70,50],
    //       },
    //   ]
    // });

    // //平均住院天数
    // var histogramChart4 = echarts.init(document.getElementById('histogramChart4'));
    // histogramChart4.setOption( {
    //   color:['#87cefa'],
    //   grid:{
    //       left: '5%',
    //       right: '5%',
    //       bottom: '5%',
    //       containLabel: true
    //   },
    //   tooltip : {
    //      trigger: 'item',
    //      formatter: "{a}<br/>{b}<br/>{c}天"
    //  },
    //   calculable : true,
    //   xAxis : [
    //       {
    //           type : 'category',
    //           data : ['厦门第一医院','厦门中山医院','厦门中医院','厦门第五医院',],
    //           axisLine:{
    //                lineStyle:{
    //                    color: '#87cefa'
    //                },
    //            },
    //            axisLabel : {
    //              interval:0,
    //              rotate:40,

    //                textStyle: {
    //                    color: '#fff',
    //                    fontSize:13
    //                }
    //            }
    //       }
    //   ],
    //   yAxis : [
    //       {
    //           type : 'value',
    //           axisLine:{
    //               lineStyle:{
    //                   color: '#87cefa'
    //               },
    //           },
    //           splitLine: {
    //               "show": false
    //           },
    //           axisLabel: {
    //               textStyle: {
    //                   color: '#fff'
    //               },
    //               formatter: function (value) {
    //                   return value + "天"
    //               },
    //           },
    //       }
    //   ],
    //   series : [
    //       {
    //           name:'平均住院天数',
    //           type:'bar',
    //           barWidth:30,
    //           data:[6,8,7,5],
    //       },
    //   ]
    // });

}
