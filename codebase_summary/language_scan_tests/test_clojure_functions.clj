;; Clojure test functions for breadcrumb detection validation

;; Basic function
(defn basic-function []
  "test")

;; Function with parameters
(defn function-with-params [param1 param2]
  (str param1 "_" param2))

;; Function without breadcrumb documentation
(defn undocumented-function []
  true)

;; Multi-arity function
(defn multi-arity-function
  ([] "no args")
  ([x] (str "one arg: " x))
  ([x y] (str "two args: " x ", " y)))

;; Function with destructuring
(defn destructuring-function [{:keys [name value]}]
  (str name ": " value))

;; Private function
(defn- private-function [x]
  (* x 2))

;; Higher-order function
(defn higher-order-function [f coll]
  (map f coll))

;; Recursive function
(defn factorial [n]
  (if (<= n 1)
    1
    (* n (factorial (dec n)))))

;; Function with pre/post conditions
(defn validated-function [x]
  {:pre [(pos? x)]
   :post [(even? %)]}
  (* x 2))

;; Macro definition
(defmacro when-valid [test body]
  `(when ~test ~body))

;; Protocol definition with methods
(defprotocol TestProtocol
  (protocol-method [this])
  (another-method [this value]))

;; Record with protocol implementation
(defrecord TestRecord [field1 field2]
  TestProtocol
  (protocol-method [this]
    (:field1 this))
  (another-method [this value]
    (assoc this :field2 value)))

;; Anonymous function examples
(def anon-function-1
  (fn [x] (* x x)))

(def anon-function-2
  #(* % %))

;; Partial application
(def add-five
  (partial + 5))

;; Memoized function
(def memoized-function
  (memoize
    (fn [x]
      (Thread/sleep 1000)
      (* x x))))

;; Atom manipulation functions
(def counter (atom 0))

(defn increment-counter []
  (swap! counter inc))

;; Undocumented utility function
(defn utility-function [data]
  (reduce + (filter even? data)))