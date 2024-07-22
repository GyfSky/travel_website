// 1.js
$(document).ready(function () {
  $(".custom-carousel").owlCarousel({
    autoWidth: true,
    loop: true
  });

  $(".custom-carousel .item").click(function () {
    $(".custom-carousel .item").not($(this)).removeClass("active");
    $(this).toggleClass("active");
  });

  $('.btn').click(function(){
    $(this).toggleClass("click");
    $('.sidebar').toggleClass("show");
  });
  $('.feat-btn').click(function(){
    $('nav ul .feat-show').toggleClass("show");
    $('nav ul .first').toggleClass("rotate");
  });
  $('.serv-btn').click(function(){
    $('nav ul .serv-show').toggleClass("show1");
    $('nav ul .second').toggleClass("rotate");
  });
  $('nav ul li').click(function(){
    $(this).addClass("active").siblings().removeClass("active");
  });
  $('.custom-btn').click(function(){
    var target = $(this).data('target');
    $('.custom-show').not(target).removeClass('show');
    $('.fas').not(target).removeClass('rotate');
    $(target).toggleClass("show");
    $('span', this).toggleClass("rotate");
  });

  // Modal for manual add
  var modal = document.getElementById("manualAddModal");
  var btn = document.getElementById("manualAdd");
  var span = document.getElementsByClassName("close")[0];

  btn.onclick = function() {
    modal.style.display = "block";
  }

  span.onclick = function() {
    modal.style.display = "none";
  }

  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }

  $('#addSpot').click(function(){
    var spotName = $('#spotName').val();
    if(spotName){
      alert("景点 '" + spotName + "' 已添加！");
      $('#spotName').val('');
      modal.style.display = "none";
    } else {
      alert("请输入景点名！");
    }
  });
});
// 为“花费最少”菜单项添加点击事件处理器
    $('#least-cost-route').click(function() {
        planRoute('least-cost');
    });

    // 为“历程最短”菜单项添加点击事件处理器
    $('#shortest-route').click(function() {
        planRoute('shortest');
    });

    // 为“全景点游”菜单项添加点击事件处理器
    $('#full-tour-route').click(function() {
        planRoute('full-tour');
    });

    function planRoute(type) {
        var locations = [];
        if (type === 'least-cost') {
            locations = [
                { name: "环翠楼", lng: 120.169118, lat: 30.239375},
                { name: "学士公园", lng: 120.155767, lat: 30.235885 },
                { name: "柳浪闻莺公园", lng: 120.156321, lat: 30.240383 },
                { name: "雷峰塔景区", lng: 120.148827, lat: 30.230929 },
                { name: "大风车", lng: 120.144133, lat: 30.226582 },
                { name: "太子湾公园", lng: 120.142181, lat: 30.225455 },
                { name: "九曜阁", lng: 120.141124, lat: 30.220779 },
                { name: "一炽松树", lng: 120.135434, lat: 30.217426 },
                { name: "挹江亭", lng: 120.142481, lat: 30.21247 },
                { name: "玉皇山景区", lng: 120.15385, lat: 30.218153 },
                { name: "西湖风景名胜区-海月亭", lng: 120.159818, lat: 30.209957 }
            ];
        } else if (type === 'shortest') {
            locations = [
                { name: "音乐喷泉观赏区", lng: 120.161087, lat: 30.253869},
                { name: "西湖外事游船", lng: 120.144956, lat: 30.229481},
                { name: "俶影桥", lng: 120.160135, lat: 30.249541 },
                { name: "涌金公园", lng: 120.160137, lat: 30.245914 },
                { name: "钱王祠", lng: 120.157914, lat: 30.242818 },
                { name: "柳浪闻莺公园", lng: 120.156321, lat: 30.240383 },
                { name: "学士公园", lng: 120.155767, lat: 30.235885 },
                { name: "环翠楼", lng: 120.169118, lat: 30.239375}
                // Add other locations for the shortest route
            ];
        } else if (type === 'full-tour') {
            locations = [
                { name: "杭州西湖风景名胜区-梅家坞", lng: 120.08702, lat: 30.202755},
                { name: "梅坞春早", lng: 120.086778, lat: 30.208214 },
                { name: "瞭望亭", lng: 120.098938, lat: 30.208838 },
                { name: "九溪十八涧", lng: 120.113339, lat: 30.202403 },
                { name: "梵音亭", lng: 120.096755, lat: 30.219031 },
                { name: "杭州西湖风景名胜区-九曲亭", lng: 120.096548, lat: 30.22622 },
                { name: "灵隐飞来峰", lng: 120.098214, lat: 30.238858 },
                { name: "杭州永福寺", lng: 120.155767, lat: 30.238962 },
                { name: "古香禅院", lng: 120.095576, lat:30.239613 }
                // Add other locations for the full tour route
            ];
        }

        var map = new AMap.Map('map-container', {
            resizeEnable: true,
            zoom: 13.4,
            center: [locations[0].lng, locations[0].lat]
        });

        // 使用高德地图的导航服务
        AMap.plugin('AMap.Driving', function() {
            var driving = new AMap.Driving({
                map: map,

            });

            // 规划多点驾车路线
            var waypoints = locations.slice(1, -1).map(function(loc) {
                return new AMap.LngLat(loc.lng, loc.lat);
            });

            var policy = AMap.DrivingPolicy.LEAST_TIME; // 默认使用最短时间
            if (type === 'least-cost') {
                policy = AMap.DrivingPolicy.LEAST_FEE;
            } else if (type === 'full-tour') {
                policy = AMap.DrivingPolicy.REAL_TRAFFIC;
            }

            driving.search(
                new AMap.LngLat(locations[0].lng, locations[0].lat),
                new AMap.LngLat(locations[locations.length - 1].lng, locations[locations.length - 1].lat),
                { waypoints: waypoints, policy: policy },
                function(status, result) {
                    if (status === 'complete') {
                        console.log('绘制驾车路线完成');
                    } else {
                        console.log('获取驾车数据失败：' + result);
                    }
                }
            );
        });
    }
