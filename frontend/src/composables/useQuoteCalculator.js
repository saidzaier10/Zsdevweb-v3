import { computed } from 'vue'

export function useQuoteCalculator(quote, options) {
    const { projectTypes, designOptions, complexityLevels, supplementaryOptions } = options

    const getSelectedProjectType = () => {
        return projectTypes.value.find(t => t.id === quote.value.project_type)
    }

    const getSelectedDesignOption = () => {
        return designOptions.value.find(o => o.id === quote.value.design_option)
    }

    const getSelectedComplexityLevel = () => {
        return complexityLevels.value.find(l => l.id === quote.value.complexity_level)
    }

    const getSelectedSupplementaryOptions = () => {
        return supplementaryOptions.value.filter(o => quote.value.supplementary_options.includes(o.id))
    }

    const total = computed(() => {
        let totalAmount = 0

        const projectType = getSelectedProjectType()
        const designOption = getSelectedDesignOption()
        const complexityLevel = getSelectedComplexityLevel()
        const suppOptions = getSelectedSupplementaryOptions()

        if (!projectType || !designOption || !complexityLevel) {
            return 0
        }

        // Convert to numbers
        totalAmount = Number(projectType.base_price) + Number(designOption.price_supplement)
        totalAmount = totalAmount * Number(complexityLevel.price_multiplier)

        // Add supplementary options
        suppOptions.forEach(option => {
            totalAmount += Number(option.price)
        })

        return Math.round(totalAmount)
    })

    return {
        getSelectedProjectType,
        getSelectedDesignOption,
        getSelectedComplexityLevel,
        getSelectedSupplementaryOptions,
        total
    }
}
