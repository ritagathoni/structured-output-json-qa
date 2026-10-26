import unittest
from src.validator import validate,business_rules,check_tool_call
class ValidationTests(unittest.TestCase):
 def test_boolean_vs_number(self): self.assertTrue(validate(True,{'type':'number'}))
 def test_required(self): self.assertTrue(validate({}, {'type':'object','required':['id']}))
 def test_business_rule(self): self.assertEqual(len(business_rules({'status':'approved','discount_pct':12,'tier1_approval':False})),2)
 def test_wrong_tool(self): self.assertIn('tool selection mismatch',check_tool_call({'name':'search_products','arguments':{}},'lookup_order',['order_id']))
if __name__=='__main__':unittest.main()
