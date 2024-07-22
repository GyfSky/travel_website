/**
 * 星空渲染
 * @param {object} galaxyCanvas 画布元素
 */
function renderGalaxy (galaxyCanvas) {
  let galaxyCtx = galaxyCanvas.getContext('2d')
  let galaxyCanvasWidth = galaxyCanvas.clientWidth
  let galaxyCanvasHeight = galaxyCanvas.clientHeight

  // 整个星空的随机星星点点位置计算
  let starDensity = 1/ 300 // 星星密度
  let starBaseNum = parseInt(galaxyCanvasWidth * galaxyCanvasHeight * starDensity) // 大概出现的星星数量
  let initStarNum = starBaseNum + Math.random() * 40 - 20 // 初始数量
  let starArr = []

  // 新增一颗星星
  let addRandomStar = function () {
    if (starArr.length > starBaseNum * 1.5) return // 5成随机波动
    let star = {
      x: parseInt(Math.random() * galaxyCanvasWidth), // 左偏移
      y: parseInt(Math.random() * galaxyCanvasHeight), // 左偏移
      r: parseInt(Math.random() > 0.01 ? 2 : 3), // 半径
      b: Math.random() > 0.5 ? Math.random() > 0.95 ? 0.80 : 0.40 : 0.25 // 随机亮度
    }
    starArr.push(star)
    renderStar(star)
  }
  // 减去一颗星星
  let reduceRandomStar = function (repeat) {
    if (starArr.length < starBaseNum * 0.5) return // 5成随机波动
    let index = parseInt(Math.random() * (starArr.length - 1))
    index = index < 0 ? 0 : index
    var star = starArr[index]
    if (star.blinking) {
      // 闪烁着的星星不删
      if (!repeat) reduceRandomStar(true)
      return
    }
    starArr.splice(index, 1)
    galaxyCtx.clearRect(star.x, star.y, star.r, star.r)
  }
  // 星星闪烁
  let starBlink = function (star) {
    let i = 1
    let blinkAnim = function () {
      if (i > 10) return
      setTimeout(blinkAnim, 200)
      if (i <= 5) {
        star.b += 0.12
      } else {
        star.b -= 0.12
      }
      renderStar(star)
      i++
    }
    blinkAnim()
  }

  // 初始化渲染星星
  for (let i = 0; i < initStarNum; i++) {
    addRandomStar()
  }

  // 随机添加或删除星星
  function autoChangeRandomStar () {
    for (let i = 0; i < 20; i++) {
      if (Math.random() < 0.5) {
        addRandomStar()
      } else {
        reduceRandomStar()
      }
    }
  }

  animRender()
  animRender2()

  // 动画帧渲染
  function animRender () {
    setTimeout(animRender, 1000)
    autoChangeRandomStar() // 随机添加或删除星星
  }

  function animRender2 () {
    setTimeout(animRender2, 1000 + Math.random() * 1000 - 500)
    // 随机星星闪烁
    var index = parseInt(Math.random() * (starArr.length - 1))
    index = index < 0 ? 0 : index
    var star = starArr[index]
    star.blinking = true
    starBlink(star)
  }

  // 渲染星星的方法
  function renderStar (star) {
    // 计算
    let imgData = galaxyCtx.createImageData(star.r, star.r)
    for (let i = 0; i < imgData.data.length; i += 4) {
      imgData.data[i + 0] = 255
      imgData.data[i + 1] = 255
      imgData.data[i + 2] = 255
      imgData.data[i + 3] = parseInt(star.b * 255)
    }
    galaxyCtx.putImageData(imgData, star.x, star.y)
  }
}

function renderMilkyWay (milkyWayCanvas) {
  // 渲染星河
  let galaxyCtx = milkyWayCanvas.getContext('2d')
  let galaxyCanvasWidth = milkyWayCanvas.clientWidth
  let galaxyCanvasHeight = milkyWayCanvas.clientHeight

  let milkyWayDeg = Math.round(Math.atan(galaxyCanvasHeight / galaxyCanvasWidth) * 180 / Math.PI, 6)
  milkyWayCanvas.style.backgroundImage = 'linear-gradient('+milkyWayDeg+'deg, rgba(255,255,255,0) 15%, rgba(255,255,255,0.05) 43%, rgba(255,255,255,0.09) 50%, rgba(255,255,255,0.05) 57%, rgba(255,255,255,0) 85%)'

  // 星河河道中随机星星位置计算
  let starDenst = 1 / 80 // 星星密度
  let riverWidth = 100 // 河道宽度
  let riverLength = parseInt(Math.sqrt(galaxyCanvasWidth ** 2 + galaxyCanvasHeight ** 2))
  let riverAngle = Math.atan(galaxyCanvasHeight / galaxyCanvasWidth)

  let mockCanvas = document.createElement('CANVAS') // 创建一个画布来描绘超长的星河图
  mockCanvas.width = riverLength * 2
  mockCanvas.height = riverWidth
  let mockCtx = mockCanvas.getContext('2d')

  let starBaseNum = parseInt(mockCanvas.width * mockCanvas.height * starDenst) // 大概出现的星星数量
  let initStarNum = starBaseNum + Math.random() * 40 - 20 // 初始数量

  let starArr = []
  let addRandomStar = function () {
    if (starArr.length > starBaseNum * 1.5) return // 5成随机波动
    let star = {
      x: parseInt(Math.random() * mockCanvas.width), // 左偏移
      y: parseInt(Math.random() * mockCanvas.height), // 左偏移
      r: parseInt(Math.random() > 0.08 ? 1 : 2), // 半径
      b: Math.random() > 0.5 ? Math.random() > 0.95 ? 0.9 : 0.25 : 0.2 // 随机亮度
    }
    starArr.push(star)
    renderStar(star)
  }

  function renderStar (star) {
    // 计算
    let imgData = mockCtx.createImageData(star.r, star.r)
    for (let i = 0; i < imgData.data.length; i += 4) {
      imgData.data[i + 0] = 255
      imgData.data[i + 1] = 255
      imgData.data[i + 2] = 255
      imgData.data[i + 3] = parseInt(star.b * 255)
    }
    mockCtx.putImageData(imgData, star.x, star.y)
  }

  for (let j = 0; j < initStarNum; j++) {
    addRandomStar(j)
  }
  let riverImgData = mockCanvas.toDataURL('image/png')
  let img = new Image()
  img.src = riverImgData
  let animTime = 0

  // 星河运动动画
  function milkyWayAnim () {
    animTime++
    if (animTime % 10 !== 0) {
      return
    }
    galaxyCtx.setTransform(1, 0, 0, 1, 0, 0)
    galaxyCtx.clearRect(0, 0, galaxyCanvasWidth, galaxyCanvasHeight)
    galaxyCtx.setTransform(1, 0, 0, 1, 0, -46)
    let spanX = animTime * 0.05 % galaxyCanvasWidth
    galaxyCtx.translate(-spanX, -spanX * galaxyCanvasHeight / galaxyCanvasWidth)
    galaxyCtx.rotate(riverAngle)
    galaxyCtx.drawImage(img, 0, 0)
  }

  animRender()

  // 动画帧渲染
  function animRender () {
    requestAnimationFrame(animRender)
    milkyWayAnim()
  }
}

/**
 * 星座描绘
 * @param constellationCanvas
 */
function renderConstellation (constellationCanvas) {
  let constellationCtx = constellationCanvas.getContext('2d')
  let canvasWidth = constellationCanvas.width
  let canvasHeight = constellationCanvas.height
  /* let starArr = [
    {x: 75, y: 5},
    {x: 75, y: 45},
    {x: 75, y: 95},
    {x: 75, y: 145},
    {x: 35, y: 50},
    {x: 115, y: 50},
    {x: 15, y: 80},
    {x: 135, y: 80}
  ]
  let lines = [
    {from: 0, to: 1},
    {from: 1, to: 2},
    {from: 2, to: 3},
    {from: 1, to: 4},
    {from: 1, to: 5},
    {from: 4, to: 6},
    {from: 5, to: 7}
  ] */

  let starArr = [
    {x: 15, y: 15},
    {x: 35, y: 55},
    {x: 15, y: 95},
    {x: 35, y: 135},
    {x: 15, y: 175},
    {x: 75, y: 215},
    {x: 115, y: 195},
    {x: 155, y: 215}
  ]
  let lines = [
    {from: 0, to: 1},
    {from: 1, to: 2},
    {from: 2, to: 3},
    {from: 3, to: 4},
    {from: 4, to: 5},
    {from: 5, to: 6},
    {from: 6, to: 7}
  ]

  function render () {
    constellationCtx.clearRect(0, 0, canvasWidth, canvasHeight)
    for (let i = 0; i < starArr.length; i++) {
      renderStar(starArr[i])
    }

    constellationCtx.beginPath()
    for (let i = 0; i < lines.length; i++) {
      renderLine(lines[i])
    }
    constellationCtx.strokeStyle = 'rgba(255,255,255,.1)'
    constellationCtx.stroke()
  }

  // 渲染星星的方法
  function renderStar (star) {
    constellationCtx.beginPath()
    let r = 1
    r += 0.15 * time
    constellationCtx.arc(star.x, star.y, r, 0, 2 * Math.PI)
    let alpha = 0.4
    alpha += 0.02 * time
    constellationCtx.fillStyle = 'rgba(255,255,255,' + alpha + ')'
    constellationCtx.shadowBlur = 0.4 * time
    constellationCtx.shadowColor = '#fff'
    // 大四角星
    constellationCtx.moveTo(star.x - 1, star.y - 1)
    constellationCtx.lineTo(star.x, star.y - 0.14 * time ** 2)
    constellationCtx.lineTo(star.x + 1, star.y - 1)
    constellationCtx.lineTo(star.x + 0.14 * time ** 2, star.y)
    constellationCtx.lineTo(star.x + 1, star.y + 1)
    constellationCtx.lineTo(star.x, star.y + 0.14 * time ** 2)
    constellationCtx.lineTo(star.x - 1, star.y + 1)
    constellationCtx.lineTo(star.x - 0.14 * time ** 2, star.y)
    constellationCtx.lineTo(star.x - 1, star.y - 1)
    // 小四角星
    constellationCtx.moveTo(star.x, star.y - 1)
    constellationCtx.lineTo(star.x + 1 + 0.06 * time ** 2, star.y - 1 - 0.06 * time ** 2)
    constellationCtx.lineTo(star.x + 1, star.y)
    constellationCtx.lineTo(star.x + 1 + 0.06 * time ** 2, star.y + 1 + 0.06 * time ** 2)
    constellationCtx.lineTo(star.x, star.y + 1)
    constellationCtx.lineTo(star.x - 1 - 0.06 * time ** 2, star.y + 1 + 0.06 * time ** 2)
    constellationCtx.lineTo(star.x - 1, star.y)
    constellationCtx.lineTo(star.x - 1 - 0.06 * time ** 2, star.y - 1 - 0.06 * time ** 2)
    constellationCtx.lineTo(star.x, star.y - 1)

    constellationCtx.fill()
  }

  // 渲染星星连线的方法
  function renderLine (line) {
    constellationCtx.moveTo(starArr[line.from].x, starArr[line.from].y)
    constellationCtx.lineTo(starArr[line.to].x, starArr[line.to].y)
  }

  let timeout
  let time = 0

  render() // 初始化

  // hover动画特效
  constellationCanvas.addEventListener('mouseenter', function () {
    clearHoverAnimTimeout()
    timeout = setInterval(function () {
      if (time >= 10) clearHoverAnimTimeout()
      time++
      render()
    }, 34)
  })
  constellationCanvas.addEventListener('mouseleave', function () {
    clearHoverAnimTimeout()
    timeout = setInterval(function () {
      if (time < 0) clearHoverAnimTimeout()
      time--
      render()
    }, 34)
  })

  function clearHoverAnimTimeout () {
    if (timeout) clearInterval(timeout)
  }
}

/**
 * 黑洞动画
 * @param nebulaCanvas 画布容器
 */
function nebulaAnim (nebulaCanvas) {
  let nebulaCtx = nebulaCanvas.getContext('2d')
  let canvasWidth = nebulaCanvas.width
  let canvasHeight = nebulaCanvas.height
  let canvasCenter = {
    x: canvasWidth / 2,
    y: canvasHeight / 2
  }

  nebulaCanvas.addEventListener('click', function () {
    // 随机生成2个起始点
    let startPoint = []
    for (let i = 0; i < 2; i++) {
      let angle = parseInt(Math.random() * 90) - 45 + 180 * i
      let y = 350 * Math.sin(angle * Math.PI / 180)
      let x = 350 * Math.cos(angle * Math.PI / 180)
      startPoint.push({
        x: x,
        y: y
      })
    }
    let time = 0
    let needTime = 1
    let tailTime = 5
    render()

    function render () {
      if (time >= needTime + tailTime) {
        nebulaCtx.clearRect(0, 0, canvasWidth, canvasHeight)
        highlightAnim()
        return
      }
      requestAnimationFrame(render)
      time++
      nebulaCtx.clearRect(0, 0, canvasWidth, canvasHeight)
      for (let i = 0; i < 2; i++) {
        let currTime = time > needTime ? needTime : time
        let currPos = {
          x: startPoint[i].x + (canvasCenter.x - startPoint[i].x) / needTime * currTime,
          y: startPoint[i].y + (canvasCenter.y - startPoint[i].y) / needTime * currTime
        }
        let currTailTime = time - tailTime < 0 ? 0 : time - tailTime
        currTailTime = currTailTime > needTime ? needTime : currTailTime
        let tailPos = {
          x: startPoint[i].x + (canvasCenter.x - startPoint[i].x) / needTime * currTailTime,
          y: startPoint[i].y + (canvasCenter.y - startPoint[i].y) / needTime * currTailTime
        }
        nebulaCtx.beginPath()
        nebulaCtx.moveTo(currPos.x, currPos.y)
        nebulaCtx.lineTo(tailPos.x, tailPos.y)
        var gnt1 = nebulaCtx.createLinearGradient(currPos.x, currPos.y, tailPos.x, tailPos.y) // 线性渐变的起止坐标
        gnt1.addColorStop(0, 'rgba(255,255,255,.5)') // 创建渐变的开始颜色，0表示偏移量，个人理解为直线上的相对位置，最大为1，一个渐变中可以写任意个渐变颜色
        gnt1.addColorStop(1, 'rgba(255,255,255,.001)')
        nebulaCtx.strokeStyle = gnt1
        nebulaCtx.stroke()
      }
    }

    // 中心光柱动画
    function highlightAnim () {
      let gnt1 = nebulaCtx.createLinearGradient(canvasCenter.x, canvasCenter.y, canvasCenter.x + 30, canvasCenter.y - 30) // 线性渐变的起止坐标
      let time = 0
      let currTime = 0

      function renderLight () {
        if (time >= 100) {
          nebulaCtx.clearRect(0, 0, canvasWidth, canvasHeight)
          return
        } else if (time >= 50) {
          currTime--
        } else {
          currTime++
        }
        requestAnimationFrame(renderLight)
        time++
        nebulaCtx.clearRect(0, 0, canvasWidth, canvasHeight)
        nebulaCtx.beginPath()
        nebulaCtx.moveTo(canvasCenter.x - 5, canvasCenter.y - 5)
        nebulaCtx.lineTo(canvasCenter.x + 25, canvasCenter.y - 35)
        nebulaCtx.lineTo(canvasCenter.x + 35, canvasCenter.y - 25)
        nebulaCtx.lineTo(canvasCenter.x + 5, canvasCenter.y + 5)
        nebulaCtx.arc(canvasCenter.x, canvasCenter.y, 10, 0, 2 * Math.PI)
        nebulaCtx.closePath()
        gnt1.addColorStop(0, 'rgba(255,255,255,' + 0.005 * currTime + ')') // 创建渐变的开始颜色，0表示偏移量，个人理解为直线上的相对位置，最大为1，一个渐变中可以写任意个渐变颜色
        gnt1.addColorStop(1, 'rgba(255,255,255,' + 0.001 * currTime + ')')
        nebulaCtx.fillStyle = gnt1
        nebulaCtx.fill()
      }

      renderLight()
    }
  })
}
