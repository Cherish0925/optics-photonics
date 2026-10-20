import gdsfactory as gf

gf.gpdk.PDK.activate()  # 使用内置通用示例 PDK
# gdsfactory 几何参数通常以微米表示
c = gf.components.straight(length=20, width=0.5)
c.write_gds("straight.gds")
