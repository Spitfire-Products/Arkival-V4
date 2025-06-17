# PowerShell test functions for breadcrumb detection validation

# Basic function
function Basic-Function {
    return "test"
}

# Function with parameters
function Function-WithParams {
    param(
        [string]$Param1,
        [int]$Param2
    )
    return "${Param1}_${Param2}"
}

# Function without breadcrumb documentation
function Undocumented-Function {
    return $true
}

# Function with mandatory parameters
function Mandatory-Params {
    param(
        [Parameter(Mandatory=$true)]
        [string]$RequiredParam,
        
        [Parameter(Mandatory=$false)]
        [int]$OptionalParam = 10
    )
    return "$RequiredParam - $OptionalParam"
}

# Function with pipeline input
function Process-Pipeline {
    param(
        [Parameter(ValueFromPipeline=$true)]
        [string]$InputObject
    )
    process {
        Write-Output "Processing: $InputObject"
    }
}

# Advanced function with CmdletBinding
function Advanced-Function {
    [CmdletBinding()]
    param(
        [string]$Name,
        [switch]$Verbose
    )
    
    if ($Verbose) {
        Write-Verbose "Verbose mode enabled"
    }
    
    Write-Output "Hello, $Name"
}

# Function with multiple parameter sets
function Multi-ParameterSet {
    [CmdletBinding(DefaultParameterSetName='ByName')]
    param(
        [Parameter(ParameterSetName='ByName')]
        [string]$Name,
        
        [Parameter(ParameterSetName='ById')]
        [int]$Id
    )
    
    switch ($PSCmdlet.ParameterSetName) {
        'ByName' { "Name: $Name" }
        'ById' { "ID: $Id" }
    }
}

# Filter function
Filter Where-LargeFile {
    if ($_.Length -gt 1MB) {
        $_
    }
}

# Function with begin/process/end blocks
function Process-Items {
    begin {
        $count = 0
    }
    process {
        $count++
        Write-Output "Item $count: $_"
    }
    end {
        Write-Output "Total items: $count"
    }
}

# Function returning custom object
function Get-CustomObject {
    param([string]$Name, [int]$Value)
    
    [PSCustomObject]@{
        Name = $Name
        Value = $Value
        Timestamp = Get-Date
    }
}

# Function with validation
function Validate-Input {
    param(
        [ValidateRange(1,100)]
        [int]$Number,
        
        [ValidateSet('Red','Green','Blue')]
        [string]$Color
    )
    
    "$Number - $Color"
}

# Recursive function
function Get-Factorial {
    param([int]$n)
    
    if ($n -le 1) {
        return 1
    } else {
        return $n * (Get-Factorial -n ($n - 1))
    }
}

# Function with error handling
function Safe-Divide {
    param(
        [double]$Numerator,
        [double]$Denominator
    )
    
    try {
        $Numerator / $Denominator
    }
    catch [System.DivideByZeroException] {
        Write-Error "Cannot divide by zero"
        return $null
    }
}

# Script block assigned to variable
$scriptBlock = {
    param($x)
    $x * 2
}

# Function using script block
function Invoke-ScriptBlock {
    param(
        [scriptblock]$ScriptBlock,
        [object[]]$ArgumentList
    )
    
    & $ScriptBlock @ArgumentList
}

# Undocumented utility function
function Utility-Function {
    Get-ChildItem -Path . -Filter *.log | 
        Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) } |
        Remove-Item -Force
}

# Function with dynamic parameters
function Dynamic-Parameters {
    [CmdletBinding()]
    param()
    
    DynamicParam {
        $paramDictionary = New-Object System.Management.Automation.RuntimeDefinedParameterDictionary
        
        $attributes = New-Object System.Management.Automation.ParameterAttribute
        $attributes.Mandatory = $false
        
        $attributeCollection = New-Object System.Collections.ObjectModel.Collection[System.Attribute]
        $attributeCollection.Add($attributes)
        
        $dynParam = New-Object System.Management.Automation.RuntimeDefinedParameter('DynamicParam', [string], $attributeCollection)
        $paramDictionary.Add('DynamicParam', $dynParam)
        
        return $paramDictionary
    }
    
    process {
        Write-Output "Dynamic parameter value: $($PSBoundParameters.DynamicParam)"
    }
}

# Class definition (PowerShell 5+)
class TestClass {
    [string]$Name
    [int]$Value
    
    TestClass([string]$name, [int]$value) {
        $this.Name = $name
        $this.Value = $value
    }
    
    [string] ToString() {
        return "$($this.Name): $($this.Value)"
    }
}

# Workflow (PowerShell 3-5)
workflow Test-Workflow {
    param([string[]]$Computers)
    
    foreach -parallel ($computer in $Computers) {
        InlineScript {
            Test-Connection -ComputerName $using:computer -Count 1
        }
    }
}