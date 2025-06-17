-- SQL test functions for breadcrumb detection validation

CREATE OR REPLACE FUNCTION basic_function()
RETURNS TEXT AS $$
BEGIN
    RETURN 'test';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION function_with_params(
    param1 TEXT,
    param2 INTEGER DEFAULT 42
)
RETURNS TEXT AS $$
BEGIN
    RETURN param1 || '_' || param2::TEXT;
END;
$$ LANGUAGE plpgsql;

-- Function without breadcrumb documentation
CREATE FUNCTION undocumented_function()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION aggregate_function(
    values NUMERIC[]
)
RETURNS NUMERIC AS $$
DECLARE
    total NUMERIC := 0;
    val NUMERIC;
BEGIN
    FOREACH val IN ARRAY values
    LOOP
        total := total + val;
    END LOOP;
    RETURN total;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION window_function_example()
RETURNS TABLE(id INTEGER, value TEXT, row_num INTEGER) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        t.id,
        t.value,
        ROW_NUMBER() OVER (ORDER BY t.id) as row_num
    FROM test_table t;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION recursive_function(n INTEGER)
RETURNS INTEGER AS $$
BEGIN
    IF n <= 1 THEN
        RETURN 1;
    ELSE
        RETURN n * recursive_function(n - 1);
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION json_function(input_json JSONB)
RETURNS JSONB AS $$
BEGIN
    RETURN jsonb_set(input_json, '{processed}', 'true'::jsonb);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION array_function(
    input_array TEXT[]
)
RETURNS TEXT[] AS $$
DECLARE
    result TEXT[] := '{}';
    item TEXT;
BEGIN
    FOREACH item IN ARRAY input_array
    LOOP
        result := array_append(result, upper(item));
    END LOOP;
    RETURN result;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION security_function(user_id INTEGER)
RETURNS TABLE(secure_data TEXT) 
SECURITY DEFINER AS $$
BEGIN
    RETURN QUERY
    SELECT sensitive_info 
    FROM secure_table 
    WHERE id = user_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION exception_function(divisor INTEGER)
RETURNS NUMERIC AS $$
BEGIN
    IF divisor = 0 THEN
        RAISE EXCEPTION 'Division by zero not allowed';
    END IF;
    RETURN 100.0 / divisor;
EXCEPTION
    WHEN division_by_zero THEN
        RAISE NOTICE 'Caught division by zero';
        RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION table_function(limit_count INTEGER)
RETURNS TABLE(
    id INTEGER,
    name TEXT,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        t.id,
        t.name,
        t.created_at
    FROM test_table t
    ORDER BY t.created_at DESC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;