class SymbolTable:
    def __init__(self):
        self.table = {}  # name → stack of values
        # كل متغير هيبقى ليه ستاك
        self.scope_stack = [[]]  # كل scope فيه أسماء variables اللي اتعرفت فيه
        self.functions = {}  # NEW
        # كل متغير هيبقى ليه ستاك وواحنا بنلف هناخد اخر واحد في الستاك
# فانكشن
    def enter_scope(self):
        self.scope_stack.append([])
# اول ما يخش قوس جديد يفتح سكوب ويعمل ابند في الستاك


    def exit_scope(self):
        # شيل كل variables اللي اتعرفت في السكوب ده
        for name in self.scope_stack[-1]:
            self.table[name].pop()  # remove last definition

            # لو مفيش تعريفات تاني → امسح الاسم خالص
            if not self.table[name]:
                del self.table[name]

        self.scope_stack.pop()
#اول ما تخرج اطلع
    def define(self, name, value):
        if name not in self.table:
            self.table[name] = []
            # لو الاسم مش موجود اعمل واحد جديد
# لو موجود اعمله بوش في الستاك بتاعه وسجله
        self.table[name].append(value)  # push
        self.scope_stack[-1].append(name)  # سجل إنه اتعرف في السكوب ده

    def lookup(self, name):
        if name in self.table and self.table[name]:
            return self.table[name][-1]  # آخر قيمة (أقرب scope)
        return None
    # لو احنا في سكوب 3 يبقى القيمة هي القيمة فيه

    def define_function(self, name, param_count):
        self.functions[name] = param_count
        # هتجيب الاسم وعدد البارميترز

    def function_exists(self, name):
        if name not in self.functions:
            return "THIS FUNCTION DOES NOT EXIST"
        else :
            return name in self.functions
# هتشوف لو موجودة في الفانكشنز ولا لا
    def debug_print(self):
        print("\n[Symbol Table -  O(1) version]")
        for name, stack in self.table.items():
            print(f"{name}: {stack}")

