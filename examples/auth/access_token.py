from bb_wrapper.wrapper.bb import BaseBBWrapper
import logging

logging.basicConfig(level=logging.DEBUG)

wrapper = BaseBBWrapper()
response = wrapper._BaseBBWrapper__authenticate()

print(response)
